from pydantic import BaseModel
import uuid
from schemas import UserInverter,ElectricalString, ElectricalStringCreate


class ProjectInverter(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    inverter_id: uuid.UUID

    inverter: UserInverter
    strings: list[ElectricalString]


class ProjectInverterCreate(BaseModel):
    inverter_id: uuid.UUID
    electrical_string: ElectricalStringCreate
