from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import Config


class UserResponse(BaseModel): # вывод пользователя
    id: int
    name: str
    role: str

    class Config:
        from_attributes = True


TaskStatus = Literal['not_started', 'in_progress', 'in_review', 'done', 'burned_down']
class TaskResponse(BaseModel): # вывод задачи
    id: int
    title: str 
    description: str 
    created_at: datetime
    dead_line: datetime
    status: TaskStatus
    user_id: int
    photo: str | None = None

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel): # вывод проекта
    id: int
    title: str
    description: str 
    created_at: datetime
    user_id: int
    tasks: List[TaskResponse]

    class Config:
        from_attributes = True