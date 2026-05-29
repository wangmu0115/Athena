from athena_matplotlib.datas import CategoricalSeriesData
from athena_matplotlib.runtime.pipeline import Pipeline
from athena_matplotlib.runtime.renderer import FigureRenderer
from athena_matplotlib.runtime.writers import NullWriter
from athena_matplotlib.specs.chart import ChartSpec
from athena_matplotlib.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
from athena_matplotlib.specs.coords.tick import TickSpec
from athena_matplotlib.specs.plots.bar import BarPlot

datas = {
    "P0": CategoricalSeriesData.from_tuples(("Q1", 12), ("Q2", 8), ("Q3", 9), ("Q4", 4)),
    "P1": CategoricalSeriesData.from_tuples(("Q1", 16), ("Q2", 4), ("Q3", 11), ("Q4", 1)),
    "P2": CategoricalSeriesData.from_tuples(("Q1", 9), ("Q2", 22), ("Q3", 7), ("Q4", 9)),
    "P3": CategoricalSeriesData.from_tuples(("Q1", 17), ("Q2", 9), ("Q3", 13), ("Q4", 3)),
    "P4": CategoricalSeriesData.from_tuples(("Q1", 22), ("Q2", 17), ("Q3", 5), ("Q4", 1)),
}
# Spec
x_axis = CartesianAxisSpec.x_axis(data_type="category", tick=TickSpec.of())
y_axis = CartesianAxisSpec.y_axis()
coord = CartesianCoord.of(x_axis, left_y_axis=y_axis)
# Plots
plots: list[BarPlot] = []
for name, data in datas.items():
    plots.append(BarPlot.of(data=data, y_axis_side="left", name=name))

spec = ChartSpec(
    title="Bar Chart Example",
    coord=coord,
    plots=plots,
    bar_layout_mode="group",
)

renderer = FigureRenderer()
writer = NullWriter()
pipeline = Pipeline(renderer, writer)
pipeline.invoke(spec)
