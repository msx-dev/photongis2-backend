from pydantic import EmailStr, BaseModel, ConfigDict
from typing import Union, Optional


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithToken(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
