from athena_charts.runtime.pipeline import Pipeline
from athena_charts.runtime.writers import FileWriter
from athena_charts.specs.charts import ChartLabels, ChartSpec
from athena_charts.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
from athena_charts.specs.plots.datas import XYSeriesData
from athena_charts.specs.plots.line import LinePlot
from athena_charts_matplotlib.renderer import MatplotlibFigureRenderer
from athena_charts_matplotlib.rendering.context import MatplotlibPipelineContext

# 使用 Matplotlib 渲染图片
renderer = MatplotlibFigureRenderer()
# 输出到文件中
writer = FileWriter(".")

pipeline = Pipeline(
    renderer,
    writer,
    context_provider=MatplotlibPipelineContext(renderer.style),
    artifact_finalizer=lambda x: x.artifact.close(),
)

chart = ChartSpec(
    labels=ChartLabels(title="CPU Usage"),
    coord=CartesianCoord(x_axis=CartesianAxisSpec.x_axis(), left_y_axis=CartesianAxisSpec.left_y_axis()),
    plots=[
        LinePlot.of(
            "bottom",
            "left",
            name="utilizations",
            z_index=100,
            data=XYSeriesData.of(
                ["05-15", "05-16", "05-17", "05-18", "05-19", "05-20", "05-21", "05-22", "05-23"],
                [
                    0.37799558142318435,
                    0.3867118322774515,
                    0.37825660878199885,
                    0.378377811846705,
                    0.3859724684768518,
                    0.3812745571236411,
                    0.3796,
                    0.38799999999999996,
                    0.3764,
                ],
            ),
        )
    ],
)


pipeline.invoke(chart, filename="test.png")
