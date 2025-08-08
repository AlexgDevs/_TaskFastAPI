from datetime import datetime
from typing import Dict, Literal, Union
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel): # Создание таска
    title: str
    description: str
    dead_line: str
    user_id: int

    @field_validator('dead_line')
    def validate_dead_line(cls, dead_line: str) -> datetime:
        try:
            dead_line = datetime.strptime(dead_line, '%Y.%m.%d')
        except ValueError:
            raise ValueError('Неверный формат даты. Используйте ГГГГ.ММ.ДД')
        
        if dead_line < datetime.now():
            raise ValueError('Дедлайн должен быть в будущем')
        
        return dead_line


class TaskPutUpdate(BaseModel): # Полное обновление таска
    title: str
    description: str
    status: str


class TaskPatchUpdate(BaseModel): # Частичное обновление таска
    title: str | None = None
    description: str | None = None
    status: str | None = None


class UserPatchUpdate(BaseModel): # Частичное обновление пользователя
    name: str | None = None
    role: str | None = None
    password: str | None = None