from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel

type SourceName = str
type SourceField = str
type FieldMapping = str | tuple[SourceName, SourceField] | Callable[[Mapping[str, BaseModel]], Any]
type SingleFieldMapping[S: BaseModel] = str | Callable[[S], Any]


def model_to_model[S: BaseModel, T: BaseModel](
    source: S,
    target_cls: type[T],
    *,
    mapping: dict[str, SingleFieldMapping[S]] | None = None,
    extra: dict[str, Any] | None = None,
    strict: bool = True,
) -> T:
    """将单个 Pydantic 模型转换为另一个 Pydantic 模型。

    字段取值规则与 `models_to_model()` 基本一致，但 `mapping` 中的可调用规则会直接接收
    当前源模型，而不是接收包含 `"__source__"` 键的字典。

    Args:
        source: 源 Pydantic 模型实例。
        target_cls: 目标 Pydantic 模型类。
        mapping: 可选的目标字段映射规则。
            `str` 表示从源模型中读取指定字段；
            `Callable` 表示接收 `source` 并动态计算目标字段值。
        extra: 可选的目标字段覆盖值，优先级高于 `mapping`。
        strict: 是否在映射阶段提前检查缺失字段并抛出 `ValueError`。

    Returns:
        通过 `target_cls.model_validate()` 校验后的目标模型实例。
    """

    adapted_mapping: dict[str, FieldMapping] | None = None
    if mapping is not None:
        adapted_mapping = {}
        for target_field_name, rule in mapping.items():
            if callable(rule):
                adapted_mapping[target_field_name] = lambda _sources, rule=rule: rule(source)
                continue

            adapted_mapping[target_field_name] = rule

    return models_to_model(
        {"__source__": source},
        target_cls,
        mapping=adapted_mapping,
        extra=extra,
        strict=strict,
    )


def models_to_model[T: BaseModel](
    sources: Mapping[str, BaseModel],
    target_cls: type[T],
    *,
    mapping: dict[str, FieldMapping] | None = None,
    extra: dict[str, Any] | None = None,
    strict: bool = True,
) -> T:
    """将多个 Pydantic 模型合并转换为一个目标 Pydantic 模型。

    字段值按以下优先级解析，越靠前优先级越高：
        1. `extra`: 如果目标字段存在于 `extra` 中，直接使用该值。
        2. `mapping`: 如果目标字段存在显式映射规则，则根据规则取值。

            - `str` 从合并后的源模型数据中读取字段。
            - `tuple[source_name, source_field]` 从指定源模型中读取字段。
            - `Callable` 接收完整的命名源模型字典，动态计算字段值。

        3. 同名字段映射：如果目标字段存在于合并后的源模型数据中，直接复制该字段值。
        4. 兜底校验：如果 `strict=True` 且目标字段为必填字段，则抛出 `ValueError`。

    Notes:
        - 源模型会先通过 `model_dump()` 转为字典。
        - 多个源模型存在同名字段时，靠后的源模型会覆盖靠前的源模型。
        - 目标模型始终通过 `target_cls.model_validate()` 创建，以保留完整校验逻辑。

    Args:
        sources: 命名源 Pydantic 模型字典。
        target_cls: 目标 Pydantic 模型类。
        mapping: 可选的目标字段映射规则。
        extra: 可选的目标字段覆盖值。
        strict: 是否在映射阶段提前检查缺失字段并抛出 `ValueError`。

    Returns:
        校验后的目标模型实例。

    Raises:
        ValueError: 未提供任何源模型，必需的源字段或目标字段缺失，映射规则引用了不存在的源模型名称。
        TypeError: 提供了不支持的映射规则类型。
    """
    if not sources:
        raise ValueError("At least one source model is required.")

    mapping = mapping or {}
    extra = extra or {}

    source_payloads = {source_name: source.model_dump() for source_name, source in sources.items()}
    merged_payload: dict[str, Any] = {}
    for payload in source_payloads.values():
        merged_payload.update(payload)

    target_payload: dict[str, Any] = {}
    for target_field_name, target_field in target_cls.model_fields.items():
        # 1. Extra override
        if target_field_name in extra:
            target_payload[target_field_name] = extra[target_field_name]
            continue

        # 2. Explicit mapping rule
        rule = mapping.get(target_field_name)
        if rule is not None:
            # 2.1 Dynamic callable mapping
            if callable(rule):
                target_payload[target_field_name] = rule(sources)
                continue

            # 2.2 Explicit source field mapping
            if isinstance(rule, tuple):
                source_name, source_field_name = rule
                if source_name not in source_payloads:
                    raise ValueError(f"Unknown source name: {source_name}.")

                source_payload = source_payloads[source_name]
                if source_field_name not in source_payload:
                    if strict:
                        raise ValueError(
                            f"Missing source field {source_field_name} from source {source_name} "
                            f"for target field {target_field_name}."
                        )
                    continue

                target_payload[target_field_name] = source_payload[source_field_name]
                continue

            # 2.3 Merged-payload field mapping
            if isinstance(rule, str):
                if rule not in merged_payload:
                    if strict:
                        raise ValueError(f"Missing source field {rule} for target field {target_field_name}.")
                    continue

                target_payload[target_field_name] = merged_payload[rule]
                continue

            raise TypeError(f"Unsupported mapping rule for target field {target_field_name}: {type(rule).__name__}.")

        # 3. Same-name field mapping
        if target_field_name in merged_payload:
            target_payload[target_field_name] = merged_payload[target_field_name]
            continue

        # 4. Required-field validation
        if strict and target_field.is_required():
            raise ValueError(
                f"Missing required target field {target_field_name} "
                f"when mapping sources {list(sources)} -> {target_cls.__name__}."
            )

    return target_cls.model_validate(target_payload)
