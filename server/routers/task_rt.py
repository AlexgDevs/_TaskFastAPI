from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

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


@task_app.get('/', response_model=List[TaskResponse])
def get_tasks():
    with Session() as session:
        tasks = session.scalars(select(Task)).all()
        return [TaskResponse.model_dump(task) for task in tasks]


@task_app.get('/{task_id}', response_model=TaskResponse)
def get_task_by_id(task_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(Task.id == task_id))
        if task:
            return TaskResponse.model_dump(task)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )


@task_app.get('/{user_id}')
def get_tasks_by_user_id(user_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(Task.user_id == user_id))
        if task:
            return TaskResponse.model_dump(task)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )


@task_app.get('/{user_id}/{task_id}')
def get_task_by_user_id(user_id: int, task_id: int):
    with Session() as session:
        task = session.scalar(select(Task).where(
            Task.id == task_id, Task.user_id == user_id))
        if task:
            return TaskResponse.model_dump(task)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )


@task_app.post('/', status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    with Session.begin() as session:
        new_task = Task(**task_data.model_dump())
        session.add(new_task)
        return {'status': 'created'}


@task_app.delete('/{task_id}')
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
