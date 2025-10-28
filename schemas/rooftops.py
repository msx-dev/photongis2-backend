from pydantic import BaseModel
import uuid


class ProjectRooftop(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    polygon: list[list[float]]
    angle: float
    slope: float


class RooftopCreate(BaseModel):
    polygon: list[list[float]]
    angle: float
    slope: float
