from typing import List
from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..schemas import ProjectResponse, TaskResponse, ProjectCreate
from ..db import Project, Task, User, Session

project_app = APIRouter(prefix='/projects', tags=['Projects'])


@project_app.get('/', response_model=List[ProjectResponse])
def projects():
    with Session() as session:
        projects = session.scalars(select(Project)).unique().all()
        return [ProjectResponse.model_validate(project) for project in projects]


@project_app.get('/{user_id}', response_model=List[ProjectResponse])
def projects_by_user(user_id: int):
    with Session() as session:
        projects = session.scalars(select(Project)
            .where(Project.user_id == user_id)
            .options(joinedload(Project.tasks))
            ).unique().all()
        return [ProjectResponse.model_validate(project) for project in projects]


@project_app.post('/', status_code=status.HTTP_201_CREATED)
def add_project(project_data: ProjectCreate):
    with Session.begin() as session:
        session.add(Project(**project_data.model_dump()))
        return {'status': 'created'}


# вот тут кароче бут таски всех один по названию удаление создание оновление | получение тасков через проект и тп


# идея кароче есть страница где можно создавать проекты и в них таски таски можно редачить менять статус (потом фотки добавлять)
