from pydantic import BaseModel, StringConstraints
from typing import Annotated
import uuid


class UserProject(BaseModel):
    id: uuid.UUID
    name: str


class ProjectCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=250)]
