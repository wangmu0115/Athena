from athena_matplotlib.datas.xy import XYSeriesData
from athena_matplotlib.options.data_label import DataLabelStyle
from athena_matplotlib.options.line_plot import DataLabelOptions, LinePlotOptions, MarkerOptions
from athena_matplotlib.options.marker import MarkerStyle
from athena_matplotlib.options.rules.conditions import DataCondition, DataPredicate
from athena_matplotlib.runtime.pipeline import Pipeline
from athena_matplotlib.runtime.renderer import FigureRenderer
from athena_matplotlib.runtime.writers import NullWriter
from athena_matplotlib.specs.chart import ChartSpec
from athena_matplotlib.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
from athena_matplotlib.specs.coords.tick import TickLabelFormatter, TickSpec
from athena_matplotlib.specs.plots.line import LinePlot

renderer = FigureRenderer()
writer = NullWriter()
pipeline = Pipeline(renderer, writer)


spec = ChartSpec(
    title="Test",
    coord=CartesianCoord.of(
        CartesianAxisSpec.x_axis("bottom", data_type="date", tick=TickSpec.of(formatter=TickLabelFormatter.date(date_format="%m-%d"))),
        left_y_axis=CartesianAxisSpec.y_axis("left", tick=TickSpec.of(TickLabelFormatter.percent())),
    ),
    plots=[
        LinePlot.of(
            data=XYSeriesData.of(
                x=[
                    "2026-05-15",
                    "2026-05-16",
                    "2026-05-17",
                    "2026-05-18",
                    "2026-05-19",
                    "2026-05-20",
                    "2026-05-21",
                    "2026-05-22",
                    "2026-05-23",
                    "2026-05-24",
                    "2026-05-25",
                ],
                y=[
                    0.3978490467274253,
                    0.40917641779379915,
                    0.40103005401651454,
                    0.3986404974273762,
                    0.4003335232732546,
                    0.39813780547206373,
                    0.3911,
                    0.3942,
                    0.38539999999999996,
                    0.3945,
                    0.3933,
                ],
            ),
            name="cpu_utilizations",
            options=LinePlotOptions.of(
                data_label=DataLabelOptions.hide().add_rule(
                    when=DataCondition.when(DataPredicate.field("last").eq(True)),
                    style=DataLabelStyle.show(
                        formatter="({name}: {y:.2%})",
                        fontsize=4,
                    ),
                ),
                marker=MarkerOptions.hide().add_rule(
                    when=DataCondition.when(DataPredicate.field("last").eq(True)),
                    style=MarkerStyle(marker="circle", markerfacecolor="red"),
                ),
            ),
        )
    ],
)


result = pipeline.invoke(spec, filename="test.png")

# print(result)
