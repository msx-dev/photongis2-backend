from pydantic import BaseModel
from typing import Optional
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


class RooftopUpdate(BaseModel):
    id: uuid.UUID
    polygon: Optional[list[list[float]]]
    angle: Optional[float]
    slope: Optional[float]
