from typing import Dict, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import Config


class UserResponse(BaseModel): # вывод пользователя
    id: int
    name: str
    role: str


TaskStatus = Literal['not_started', 'in_progress', 'in_review', 'done', 'burned_down']
class TaskResponse(BaseModel): # вывод задачи
    id: int
    title: str 
    description: str 
    created_at: datetime
    dead_line: datetime
    status: TaskStatus
    user_id: int

    class Config:
        from_attributes = True