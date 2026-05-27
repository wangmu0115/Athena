# from athena_matplotlib.rendering.axes_runtime import AxesRuntime


# def apply_cartesian_legend(
#     axes_runtime: AxesRuntime,
#     *,
#     # options: "RenderFigureOptions",
# ) -> None:
#     legend_options = getattr(options, "legend", None)
#     if legend_options is not None and legend_options.visible is False:
#         return

#     handles = []
#     labels = []

#     for ax in axes_runtime.all_axes:
#         ax_handles, ax_labels = ax.get_legend_handles_labels()
#         for handle, label in zip(ax_handles, ax_labels):
#             if not label or label.startswith("_"):
#                 continue
#             handles.append(handle)
#             labels.append(label)

#     if not handles:
#         return

#     legend_params = {}

#     if legend_options is not None:
#         legend_params.update(
#             legend_options.model_dump(
#                 exclude_none=True,
#                 exclude={"visible"},
#                 by_alias=True,
#             )
#         )

#     axes_runtime.axes.legend(
#         handles,
#         labels,
#         **legend_params,
#     )
