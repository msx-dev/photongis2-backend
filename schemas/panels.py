from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
import uuid


class UserPanel(BaseModel):
    id: uuid.UUID
    name: str
    height: Annotated[int, Field(ge=0)]
    width: Annotated[int, Field(ge=0)]
    power: Annotated[int, Field(ge=0)]


class PanelCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    height: Annotated[int, Field(ge=0)]
    width: Annotated[int, Field(ge=0)]
    power: Annotated[int, Field(ge=0)]
