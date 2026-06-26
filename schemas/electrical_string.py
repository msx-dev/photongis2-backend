from pydantic import BaseModel
import uuid

class ElectricalString(BaseModel):
    id: uuid.UUID
    project_inverter_id: uuid.UUID
    design_lines: list[list[list[float]]]
    connected_polygons: list[str]


class ElectricalStringCreate(BaseModel):
    design_lines: list[list[list[float]]]
    connected_polygons: list[str]