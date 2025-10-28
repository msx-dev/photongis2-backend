from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional
import uuid


class UserProject(BaseModel):
    id: uuid.UUID
    name: str


class ProjectCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]


class ProjectUpdate(BaseModel):
    id: uuid.UUID
    name: Optional[str]
