from typing import Dict, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import Config

from sqlmodel import SQLModel


class UserResponse(BaseModel):
    id: int
    name: str
    role: str


TaskStatus = Literal['not_started', 'in_progress', 'in_review', 'done']
class TaskResponse(BaseModel):
    id: int
    title: str 
    description: str 
    created_at: datetime 
    status: TaskStatus
    user_id: int

    class Config:
        from_attributes = True