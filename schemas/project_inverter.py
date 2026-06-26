from pydantic import BaseModel
import uuid

from schemas.electrical_string import ElectricalStringCreate


class ProjectInverter(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    inverter_id: uuid.UUID


class ProjectInverterCreate(BaseModel):
    inverter_id: uuid.UUID
    electrical_string: ElectricalStringCreate