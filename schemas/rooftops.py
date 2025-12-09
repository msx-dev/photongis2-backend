from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid


class Panel(BaseModel):
    x: int
    y: int
    coords: list[list[float]]


class ProjectRooftop(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    additional_panels: Dict[str, Panel]
    initial_polygon: list[list[float]]
    transformed_additional_panels: Dict[str, Panel]
    angle: float
    slope: float
    solar_production: Optional[dict] = None
    spacing: int
    width: int
    height: int
    power: int
    name: str


class RooftopCreate(BaseModel):
    additional_panels: Dict[str, Panel]
    initial_polygon: list[list[float]]
    transformed_additional_panels: Dict[str, Panel]
    spacing: int
    angle: float
    slope: float
    panel_id: uuid.UUID


class RooftopUpdate(BaseModel):
    additional_panels: Optional[Dict[str, Panel]] = None
    initial_polygon: Optional[List[List[float]]] = None
    transformed_additional_panels: Optional[Dict[str, Panel]] = None
    spacing: Optional[int] = None
    angle: Optional[float] = None
    slope: Optional[float] = None
