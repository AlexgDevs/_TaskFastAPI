from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from datetime import datetime

from ..db import (
    Task,
    Session,
    User
)
from ..schemas import (
    TaskCreate,
    TaskPatchUpdate,
    TaskPutUpdate,
    TaskResponse
)


task_app = APIRouter(prefix='/tasks', tags=['Tasks'])


# кароче получение всех тасков
@task_app.get('/', response_model=List[TaskResponse])  # all
def get_tasks():
    with Session() as session:
        tasks = session.scalars(select(Task)).all()
        return [TaskResponse.model_validate(task) for task in tasks]


# получение всех тасков по конкретному пользователю
@task_app.get('/{user_id}', response_model=List[TaskResponse])  # all
def get_tasks_by_user_id(user_id: int, status: str = Query(None)):
    with Session() as session:
        if status:
            tasks = session.scalars(select(Task).where(
                Task.user_id == user_id,
                Task.status == status
            )).all()
        else:
            tasks = session.scalars(select(Task).where(
                Task.user_id == user_id,
            )).all()

        return [TaskResponse.model_validate(task) for task in tasks]


# получение конкретного таска
@task_app.get('/{task_id}', response_model=TaskResponse)  # one
def get_task_by_id(task_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(Task.id == task_id))
        if task:
            return TaskResponse.model_validate(task)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )


# получение конкретного таска конкретного пользователя
@task_app.get('/{user_id}/{task_id}', response_model=TaskResponse)  # one
def get_task_by_user_id(user_id: int, task_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(
            Task.id == task_id, Task.user_id == user_id))
        if task:
            return TaskResponse.model_validate(task)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )


# создание таска
@task_app.post('/', status_code=status.HTTP_201_CREATED)  # post
def create_task(task_data: TaskCreate):
    with Session.begin() as session:
        new_task = Task(**task_data.model_dump())
        session.add(new_task)
        return {'status': 'created'}


# удаление таска
@task_app.delete('/{task_id}')  # del
def delete_task(task_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(Task.id == task_id))
        if task:
            session.delete(task)
            return {'status': 'deleted'}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )
