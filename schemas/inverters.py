from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
import uuid


class UserInverter(BaseModel):
    id: uuid.UUID
    name: str
    max_ac_power: Annotated[int, Field(gt=0)]
    max_dc_power: Annotated[int, Field(gt=0)]
    max_dc_voltage: Annotated[int, Field(gt=0)]
    mppt_min_voltage: Annotated[int, Field(gt=0)]
    mppt_max_voltage: Annotated[int, Field(gt=0)]
    start_voltage: Annotated[int | None, Field(gt=0)] = None
    max_current_per_mppt: Annotated[float | None, Field(ge=0)] = None
    mppt_count: Annotated[int | None, Field(gt=0)] = None
    max_strings_per_mppt: Annotated[int | None, Field(gt=0)] = None
    efficiency: Annotated[float | None, Field(gt=0, le=1)] = None



class InverterCreate(BaseModel):
    name: str
    max_ac_power: Annotated[int, Field(gt=0)]
    max_dc_power: Annotated[int, Field(gt=0)]
    max_dc_voltage: Annotated[int, Field(gt=0)]
    mppt_min_voltage: Annotated[int, Field(gt=0)]
    mppt_max_voltage: Annotated[int, Field(gt=0)]
    start_voltage: Annotated[int | None, Field(gt=0)] = None
    max_current_per_mppt: Annotated[float | None, Field(ge=0)] = None
    mppt_count: Annotated[int | None, Field(gt=0)] = None
    max_strings_per_mppt: Annotated[int | None, Field(gt=0)] = None
    efficiency: Annotated[float | None, Field(gt=0, le=1)] = None
