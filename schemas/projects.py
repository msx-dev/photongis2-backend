from pydantic import BaseModel


class UserProject(BaseModel):
    name: str
