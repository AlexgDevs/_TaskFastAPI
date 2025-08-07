from typing import Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


from sqlmodel import SQLModel


class UserResponse(BaseModel):
    id: int
    name: str
    role: str


class TaskResponse(BaseModel):
    id: int
    title: str 
    description: str 
    created_at: datetime 
    status: str 
    user_id: int