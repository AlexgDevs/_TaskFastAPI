from typing import Dict, Literal, Union
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int


class TaskPutUpdate(BaseModel):
    title: str
    description: str
    status: str


class TaskPatchUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class UserPatchUpdate(BaseModel):
    id: int | None = None
    name: str | None = None
    role: str | None = None
    password: str | None = None