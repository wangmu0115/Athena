from typing import Annotated

from pydantic import Field

from athena_charts.specs.coords.cartesian import CartesianCoord
from athena_charts.specs.coords.polar import PolarCoord

type CoordSpec = Annotated[CartesianCoord | PolarCoord, Field(discriminator="kind")]
