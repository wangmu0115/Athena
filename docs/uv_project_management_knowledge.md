# uv 项目管理知识点

这份文档结合 Athena 和 Midas 两个项目整理 uv 项目管理知识。Athena 代表“可发布的单包工具库”，Midas 代表“多成员 workspace 业务项目”。目标是让你能从零开始构建 uv 项目，并知道什么时候该用单包、workspace、extras、dependency groups、build、publish 和 Docker/CI 安装方式。

## 0. 先建立整体模型

uv 不是单纯的 `pip` 替代品。它在一个工具里覆盖了 Python 版本选择、虚拟环境、依赖解析、锁文件、命令运行、包构建和包发布。

现代 uv 项目的核心文件通常是：

```text
project/
├── pyproject.toml
├── uv.lock
├── .python-version
├── README.md
├── src/
├── tests/
└── docs/
```

最重要的概念：

- `pyproject.toml`：项目的中心配置，包含元数据、依赖、构建系统、工具配置。
- `uv.lock`：锁定后的完整依赖解析结果，保证不同机器安装出一致环境。
- `.python-version`：本项目希望使用的 Python 版本。
- `.venv`：uv 默认创建和维护的项目虚拟环境。
- `src/` layout：推荐的包源码布局，可以减少“当前目录误导导入”的问题。
- distribution name：安装名，例如 `athena-kit`。
- import package name：导入名，例如 `athena_kit`。
- workspace：一个仓库里多个 Python 项目共享锁文件和解析结果。

## 1. 最小可用知识点

如果你只想立刻能创建、安装、运行、测试一个 uv 项目，先掌握这一节就够。

### 1.1 创建普通应用项目

适合脚本、简单服务、实验项目：

```bash
uv init my-app
cd my-app
uv add pydantic
uv run main.py
```

典型 `pyproject.toml`：

```toml
[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
]
```

普通应用默认不一定是可安装包，也不一定需要 `[build-system]`。如果你只是运行 `main.py`，这是最轻量的形态。

### 1.2 创建可打包项目

适合库、CLI、Web API、需要测试目录和 `src/` 结构的项目：

```bash
uv init --package my-package
cd my-package
uv add pydantic
uv add --dev pytest ruff
uv sync
uv run pytest
uv run ruff check
uv build
```

典型结构：

```text
my-package/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── my_package/
│       └── __init__.py
└── tests/
```

### 1.3 常用命令速记

```bash
# 安装或同步依赖到 .venv
uv sync

# 添加运行时依赖，写入 project.dependencies
uv add httpx

# 添加开发依赖，写入 dependency-groups.dev
uv add --dev pytest ruff

# 删除依赖
uv remove httpx

# 在项目虚拟环境里运行命令
uv run python
uv run pytest
uv run ruff check

# 更新锁文件
uv lock

# 检查锁文件是否过期，适合 CI
uv lock --check

# 构建发布产物
uv build

# 发布到包索引
uv publish
```

### 1.4 最小 pyproject 该看懂哪些字段

```toml
[project]
name = "athena-kit"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.13.4",
]

[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "ruff>=0.15.12",
]
```

理解方式：

- `name` 是安装名，用户执行 `uv add athena-kit` 时用它。
- `version` 是发布版本。
- `requires-python` 限定项目支持的 Python 版本。
- `dependencies` 是运行项目必须安装的依赖，会进入发布元数据。
- `[build-system]` 决定如何把项目构建成 wheel/sdist。
- `[dependency-groups].dev` 是本地开发工具依赖，不会成为用户安装你的包时的运行依赖。

## 2. Athena 项目给你的知识点

Athena 是一个可发布的单包工具库。它的根 `pyproject.toml` 展示了一个库项目应该具备的完整骨架。

### 2.1 单包库的配置形态

Athena 的核心配置：

```toml
[project]
name = "athena-kit"
version = "1.0.0"
description = "A modular Python toolkit for Athena projects."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.13.4",
]

[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"
```

这里有一个重要命名差异：

```text
安装名：athena-kit
导入名：athena_kit
```

Python 包发布时常用短横线命名 distribution，代码导入时使用下划线命名 import package。

### 2.2 extras：把可选能力拆出去

Athena 把 dataframe、http、lark、matplotlib 做成可选依赖：

```toml
[project.optional-dependencies]
dataframe = [
    "pandas>=2.3.3",
]
http = [
    "httpx>=0.28.1",
]
lark = [
    "httpx>=0.28.1",
]
matplotlib = [
    "matplotlib>=3.10.9",
]
all = [
    "httpx>=0.28.1",
    "matplotlib>=3.10.9",
    "pandas>=2.3.3",
]
```

用户可以按需安装：

```bash
uv add athena-kit
uv add "athena-kit[http]"
uv add "athena-kit[lark,dataframe]"
uv add "athena-kit[all]"
```

什么时候用 extras：

- 某个功能不是所有用户都需要。
- 依赖比较重，例如 pandas、matplotlib。
- 依赖只属于某个插件式功能。
- 你希望默认安装保持轻量。

不要把 `pytest`、`ruff`、`mypy` 这类开发工具放进 extras。它们属于 dependency groups。

### 2.3 开发命令

Athena README 里的开发流：

```bash
uv sync --extra all
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run pytest tests
```

这里 `--extra all` 表示把所有可选功能依赖也装上，适合跑完整测试。

### 2.4 发布流程

Athena README 里的发布流：

```bash
uv sync --extra all
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run pytest tests
uv build
uv publish
```

发布前应检查：

- `pyproject.toml` 的版本号已经更新。
- 包内 `__version__` 如果存在，也和 `pyproject.toml` 一致。
- README、LICENSE、classifiers、project.urls 信息完整。
- `uv build` 能产出 `dist/*.whl` 和 `dist/*.tar.gz`。
- 最好用 `uv build --no-sources` 验证包不依赖本地 uv source 配置。

## 3. Midas 项目给你的知识点

Midas 是一个 uv workspace。它把业务核心包、API 应用、notebook 探索环境放在同一个仓库里管理。

### 3.1 workspace 根项目

Midas 根 `pyproject.toml`：

```toml
[project]
name = "midas-workspace"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = false

[tool.uv.workspace]
members = [
    "packages/midas",
    "apps/midas-api",
    "notebooks",
]

[tool.uv.sources]
midas = { workspace = true }
midas-api = { workspace = true }
midas-notebooks = { workspace = true }
```

解释：

- `midas-workspace` 是管理入口，不是要发布的包。
- `package = false` 表示根项目不作为 Python package 安装。
- `members` 列出 workspace 成员。
- workspace 共享一个 `uv.lock`。
- `tool.uv.sources` 告诉 uv：这些包来自本地 workspace，不去 PyPI 找。

### 3.2 workspace 成员

Midas 当前成员：

```text
Midas/
├── pyproject.toml
├── uv.lock
├── packages/
│   └── midas/
│       └── pyproject.toml
├── apps/
│   └── midas-api/
│       └── pyproject.toml
└── notebooks/
    └── pyproject.toml
```

`packages/midas` 是业务核心包：

```toml
[project]
name = "midas"
dependencies = [
    "akshare>=1.18.59",
    "athena-kit[dataframe,lark]>=1.0.0",
    "pydantic>=2.13.4",
    "pydantic-settings>=2.14.0",
    "python-dotenv>=1.2.2",
]

[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"
```

`apps/midas-api` 是 API 应用包：

```toml
[project]
name = "midas-api"
dependencies = [
    "fastapi>=0.115.0",
    "midas>=0.1.0",
    "uvicorn[standard]>=0.30.0",
]

[project.scripts]
midas-api = "midas_api.main:run"

[tool.uv.sources]
midas = { workspace = true }
```

`notebooks` 是非发布成员：

```toml
[project]
name = "midas-notebooks"
dependencies = [
    "ipykernel>=6.29.0",
    "jupyterlab>=4.2.0",
    "midas>=0.1.0",
]

[tool.uv]
package = false

[tool.uv.sources]
midas = { workspace = true }
```

### 3.3 workspace 常用命令

在 Midas 根目录：

```bash
# 同步所有 workspace 成员
uv sync --all-packages

# 只同步 API 应用及其依赖
uv sync --package midas-api

# 生产/Docker 场景，不装 dev 依赖
uv sync --package midas-api --no-dev

# 生产/Docker 场景，非 editable 安装本地 workspace 包
uv sync --package midas-api --no-dev --no-editable

# 给指定成员添加依赖
uv add --package midas pydantic-settings
uv add --package midas-api fastapi

# 运行指定成员的脚本入口
uv run --package midas-api midas-api

# 运行 workspace 测试和 lint
uv run pytest
uv run ruff check
```

### 3.4 什么时候用 workspace

适合：

- 一个仓库里有多个强相关包。
- 业务核心、API、CLI、worker、notebook 需要共享代码。
- 多个成员要一起开发、一起测试。
- 希望本地依赖自动 editable，改核心包后 API 立刻看到变化。

不适合：

- 每个项目需要完全不同的 Python 版本。
- 子项目之间依赖冲突明显。
- 子项目独立发版、独立部署、几乎不会一起修改。
- 你希望每个子项目有完全独立的虚拟环境和 lockfile。

## 4. 最全知识点地图

这一节按主题列出 uv 项目管理应该掌握的完整知识。

### 4.1 项目类型

普通应用：

- `uv init my-app`
- 默认适合脚本和轻量应用。
- 不一定安装自身为 package。
- 可用 `uv run main.py` 运行。

可打包应用：

- `uv init --package my-api`
- 有 `src/` 布局。
- 可以定义 `[project.scripts]`。
- 适合 CLI、FastAPI 服务、worker。

库项目：

- `uv init --lib my-lib`
- 关注可复用、可发布、API 稳定。
- 需要 README、LICENSE、classifiers、类型声明等发布元数据。

workspace：

- 根项目管理多个成员。
- 每个成员有自己的 `pyproject.toml`。
- 整个 workspace 共享一个 `uv.lock`。
- 用 `uv run --package <name>` 或 `uv sync --package <name>` 操作指定成员。

### 4.2 依赖分类

运行时依赖：

```toml
[project]
dependencies = [
    "pydantic>=2.13.4",
]
```

可选功能依赖：

```toml
[project.optional-dependencies]
http = [
    "httpx>=0.28.1",
]
```

开发依赖：

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "ruff>=0.15.12",
]
```

替代依赖来源：

```toml
[tool.uv.sources]
midas = { workspace = true }
foo = { path = "../foo" }
bar = { git = "https://github.com/example/bar" }
```

判断规则：

- 用户安装你的包时必须有：放 `project.dependencies`。
- 用户按功能选择安装：放 `project.optional-dependencies`。
- 只有开发者需要：放 `dependency-groups`。
- 依赖从本地 path、workspace、git、私有 index 来：写 `tool.uv.sources`。

### 4.3 dependency groups 和 extras 的区别

| 配置 | 是否进入发布元数据 | 典型用途 | 示例 |
| --- | --- | --- | --- |
| `project.dependencies` | 是 | 运行必需依赖 | `pydantic` |
| `project.optional-dependencies` | 是 | 用户可选功能 | `athena-kit[lark]` |
| `dependency-groups` | 否 | 本地开发、测试、lint | `pytest`, `ruff` |
| `tool.uv.sources` | 否，uv 开发解析用 | workspace/path/git/index | `midas = { workspace = true }` |

### 4.4 lock 和 sync

`uv.lock` 是解析结果；`.venv` 是实际安装环境。

```bash
# 解析并写入 lockfile
uv lock

# 检查 lockfile 是否和 pyproject 匹配
uv lock --check

# 按 lockfile 同步 .venv
uv sync

# CI 中要求不修改 lockfile
uv sync --locked

# 完全按已有 lockfile 使用，不检查是否过期
uv sync --frozen
```

实用理解：

- `uv run` 通常会自动 lock 和 sync。
- 新版本包发布不会自动让 lockfile 过期；要显式升级。
- CI 推荐用 `--locked`，避免流水线悄悄改锁文件。
- Docker 推荐用 `--no-dev`，只装生产依赖。

### 4.5 运行命令

```bash
# 运行 Python
uv run python

# 运行模块
uv run python -m my_package

# 运行工具
uv run pytest
uv run ruff check

# 临时带一个依赖运行，不写入项目依赖
uv run --with jupyter jupyter lab

# workspace 中运行指定成员的脚本
uv run --package midas-api midas-api
```

### 4.6 构建系统

Athena 和 Midas 都使用 `uv_build`：

```toml
[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"
```

构建命令：

```bash
uv build
uv build --package midas
uv build --package midas-api
uv build --no-sources
```

`--no-sources` 很适合发布前验证：确保包不依赖本地 workspace/path/git 配置才能构建。

### 4.7 入口命令

Midas API 使用：

```toml
[project.scripts]
midas-api = "midas_api.main:run"
```

安装后或 `uv run` 环境中可以执行：

```bash
uv run --package midas-api midas-api
```

规则：

- 左边 `midas-api` 是命令名。
- 右边 `midas_api.main:run` 是 Python 函数。
- 使用 entry point 的项目需要有构建系统。

### 4.8 Docker/生产安装

Midas README 的 Docker 思路：

```dockerfile
RUN uv sync --package midas-api --no-dev --no-editable
CMD ["uv", "run", "--package", "midas-api", "midas-api"]
```

含义：

- `--package midas-api`：只安装 API 应用需要的成员。
- `--no-dev`：不要测试、lint 等开发依赖。
- `--no-editable`：以接近生产的方式安装本地包。

### 4.9 版本管理

常见方式：

```bash
uv version
uv version 1.0.1
uv version --bump patch
uv version --bump minor
uv version --bump major
```

建议：

- 库项目发布前必须明确更新版本。
- 如果源码里有 `__version__`，保持它和 `pyproject.toml` 一致。
- 应用项目也可以版本化，便于部署追踪。

### 4.10 代码质量工具

Athena 和 Midas 都把 ruff 放在 dev group：

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "ruff>=0.15.12",
]

[tool.ruff]
line-length = 120
target-version = "py312"
```

常用命令：

```bash
uv run ruff check
uv run ruff check --fix
uv run ruff format
uv run ruff format --check
uv run pytest
```

### 4.11 Python 版本

两个项目都使用 Python 3.12：

```text
.python-version: 3.12
requires-python = ">=3.12"
```

区别：

- `.python-version` 是本地开发环境提示。
- `requires-python` 是项目元数据和依赖解析约束。

workspace 中要特别小心 Python 版本。uv workspace 会把所有成员的 `requires-python` 取交集，如果成员之间版本要求差异太大，workspace 会很难维护。

### 4.12 私有源、git、path、workspace source

常见 source：

```toml
[tool.uv.sources]
local-lib = { path = "../local-lib" }
remote-lib = { git = "https://github.com/org/remote-lib" }
midas = { workspace = true }
```

注意：

- `tool.uv.sources` 主要服务本地开发解析，不是标准发布元数据。
- 发布前用 `uv build --no-sources` 或 `uv lock --no-sources` 验证更稳。
- workspace source 依赖在本地通常是 editable 的。

### 4.13 项目文档应该写什么

最少要写：

```markdown
## 安装
uv sync

## 开发
uv run ruff check
uv run pytest

## 运行
uv run --package midas-api midas-api

## 发布
uv build
uv publish
```

库项目还要写：

- 用户如何安装默认依赖。
- 用户如何安装 extras。
- 每个 extra 对应什么功能。
- 发布和版本策略。

workspace 项目还要写：

- 每个 member 的职责。
- 常用 `--package` 命令。
- Docker/CI 如何只安装目标应用。
- 本地 workspace 依赖关系图。

## 5. 从零构建项目的路线

### 5.1 从零构建 Athena 类型的工具库

```bash
uv init --lib athena-kit
cd athena-kit
uv add pydantic
uv add --dev pytest ruff
```

调整 `pyproject.toml`：

```toml
[project]
name = "athena-kit"
version = "0.1.0"
description = "A reusable Python toolkit."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.13.4",
]

[project.optional-dependencies]
http = [
    "httpx>=0.28.1",
]
all = [
    "httpx>=0.28.1",
]

[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "ruff>=0.15.12",
]
```

开发验证：

```bash
uv sync --extra all
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest
uv build
```

### 5.2 从零构建 Midas 类型的 workspace

```bash
mkdir my-workspace
cd my-workspace
uv init --bare

uv init --package packages/my-core
uv init --package apps/my-api
uv init notebooks
```

根 `pyproject.toml`：

```toml
[project]
name = "my-workspace"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = false

[tool.uv.workspace]
members = [
    "packages/my-core",
    "apps/my-api",
    "notebooks",
]

[tool.uv.sources]
my-core = { workspace = true }
my-api = { workspace = true }
my-notebooks = { workspace = true }

[dependency-groups]
dev = [
    "pytest",
    "ruff",
]
```

`apps/my-api/pyproject.toml`：

```toml
[project]
name = "my-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "my-core>=0.1.0",
    "uvicorn[standard]",
]

[project.scripts]
my-api = "my_api.main:run"

[build-system]
requires = ["uv_build>=0.9.25,<0.12.0"]
build-backend = "uv_build"

[tool.uv.sources]
my-core = { workspace = true }
```

常用命令：

```bash
uv sync --all-packages
uv add --package my-core pydantic
uv add --package my-api fastapi
uv run --package my-api my-api
uv run pytest
uv run ruff check
```

## 6. Athena 和 Midas 的可借鉴实践

Athena 值得借鉴：

- 使用 `src/` layout。
- 用 `uv_build` 做构建后端。
- 把重依赖放进 extras，默认安装保持轻量。
- README 写清楚每个 extra 的安装方式。
- 发布前执行 sync、lint、format check、test、build、publish。

Midas 值得借鉴：

- 根项目 `package = false`，只做 workspace 管理入口。
- 核心业务包 `midas`、API 应用 `midas-api`、notebook 环境独立成成员。
- 用 `tool.uv.sources` 把成员依赖解析到本地 workspace。
- Docker 只安装目标应用：`uv sync --package midas-api --no-dev --no-editable`。
- README 给出 `uv run --package midas-api midas-api` 这样的精确运行命令。

## 7. 常见坑

- 把开发工具写进 `project.dependencies`：会导致用户安装你的包时也安装 pytest、ruff。
- 忘记提交 `uv.lock`：团队和 CI 可能解析出不同版本。
- 在 workspace 成员之间只写依赖名但忘记 `tool.uv.sources`：uv 可能去 PyPI 找包。
- 修改 `pyproject.toml` 后没有更新 lockfile：CI 用 `--locked` 会失败。
- 发布库时依赖本地 path/workspace source：用户在 PyPI 安装时无法复现。
- extras 命名不清晰：用户不知道该安装哪个功能。
- workspace 成员职责过碎：维护成本变高。
- workspace 成员依赖互相循环：构建、测试、发布都会变麻烦。

## 8. 学习顺序

1. 先读 Athena 根 `pyproject.toml`，理解单包库。
2. 再读 Athena README 的安装、开发、发布命令。
3. 读 Midas 根 `pyproject.toml`，理解 workspace root。
4. 读 `packages/midas/pyproject.toml`，理解核心业务包。
5. 读 `apps/midas-api/pyproject.toml`，理解应用入口和 workspace 依赖。
6. 读 `notebooks/pyproject.toml`，理解非发布成员。
7. 对照 uv 官方文档补齐依赖、lock、sync、workspace、build、publish。

## 9. 参考文档

项目内文档：

- Athena `README.md`
- Athena `pyproject.toml`
- Midas `README.md`
- Midas `pyproject.toml`
- Midas `packages/midas/pyproject.toml`
- Midas `apps/midas-api/pyproject.toml`
- Midas `notebooks/pyproject.toml`
- Midas `docs/python-project-knowledge-base.md`

uv 官方文档：

- uv Projects: https://docs.astral.sh/uv/concepts/projects/
- Creating projects: https://docs.astral.sh/uv/concepts/projects/init/
- Managing dependencies: https://docs.astral.sh/uv/concepts/projects/dependencies/
- Running commands: https://docs.astral.sh/uv/concepts/projects/run/
- Locking and syncing: https://docs.astral.sh/uv/concepts/projects/sync/
- Configuring projects: https://docs.astral.sh/uv/concepts/projects/config/
- Using workspaces: https://docs.astral.sh/uv/concepts/projects/workspaces/
- Building and publishing packages: https://docs.astral.sh/uv/guides/package/
- uv command reference: https://docs.astral.sh/uv/reference/cli/

Python Packaging 相关标准：

- PyPA dependency specifiers: https://packaging.python.org/en/latest/specifications/dependency-specifiers/
- PyPA pyproject.toml guide: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- PEP 621 project metadata: https://peps.python.org/pep-0621/
- PEP 735 dependency groups: https://peps.python.org/pep-0735/
