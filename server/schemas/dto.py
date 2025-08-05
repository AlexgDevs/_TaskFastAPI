from typing import Dict
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    name: str
    role: str


class TaskResponse(BaseModel):
    title: str
    description: str
    user: UserResponse

