from typing import List
from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..schemas import ProjectResponse, TaskResponse, ProjectCreate, ProjectPatchUpdate
from ..db import Project, Task, User, Session

project_app = APIRouter(prefix='/projects', tags=['Projects'])


# получение всех проектов
@project_app.get('/', response_model=List[ProjectResponse])
def projects():
    with Session() as session:
        projects = session.scalars(select(Project)).unique().all()
        return [ProjectResponse.model_validate(project) for project in projects]


# получениче всех проектов конкретного пользователя
@project_app.get('/{user_id}', response_model=List[ProjectResponse])
def projects_by_user(user_id: int):
    with Session() as session:
        projects = session.scalars(select(Project)
                                .where(Project.user_id == user_id)
                                .options(joinedload(Project.tasks))
                                ).unique().all()
        return [ProjectResponse.model_validate(project) for project in projects]


# создание проекта
@project_app.post('/', status_code=status.HTTP_201_CREATED)
def add_project(project_data: ProjectCreate):
    with Session.begin() as session:
        session.add(Project(**project_data.model_dump()))
        return {'status': 'created'}


@project_app.patch('/{user_id}/{project_id}')
def change_project_by_user(user_id: int, project_id: int, project_data: ProjectPatchUpdate):
    with Session.begin() as session:
        project = session.scalar(select(Project).where(
            Project.id == project_id, Project.user_id == user_id))
        if project:
            update_data = project_data.model_dump(exclude_unset=True)
            session.merge(Project(id=project_id, **update_data))
            return {'status': 'updated'}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project not found'
            )


@project_app.delete('/{user_id}/{project_id}')
def delete_project_by_user(user_id: int, project_id: int):
    with Session.begin() as session:
        project = session.scalar(select(Project)
                                .where(Project.id == project_id, Project.user_id == user_id))
        if project: 
            session.delete(project)
            return {'status': 'deleted'}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project not found'
            )
