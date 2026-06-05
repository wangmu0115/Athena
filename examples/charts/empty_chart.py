from athena_kit.matplotlib.runtime.pipeline import Pipeline
from athena_kit.matplotlib.runtime.renderer import FigureRenderer
from athena_kit.matplotlib.runtime.writers import FileWriter
from athena_kit.matplotlib.specs.chart import ChartSpec
from athena_kit.matplotlib.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord

renderer = FigureRenderer()
writer = FileWriter(".")
pipeline = Pipeline(renderer, writer)

spec = ChartSpec(
    title="Test",
    coord=CartesianCoord.of(
        CartesianAxisSpec.x_axis("bottom", data_type="datetime"),
        left_y_axis=CartesianAxisSpec.y_axis("left"),
    ),
)

result = pipeline.invoke(spec, filename="test.png")

print(result)
