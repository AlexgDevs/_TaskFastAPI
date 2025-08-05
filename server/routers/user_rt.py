from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from ..db import (
    Session,
    User
)
from ..schemas import (
    UserResponse,
    UserPatchUpdate
)


user_app = APIRouter(prefix='/users', tags=['Users'])


@user_app.get('/', response_model=List[UserResponse])
def get_users():
    with Session() as session:
        users = session.scalars(select(User)).all()
        users_data = [UserResponse.model_dump(user) for user in users]
        return users_data


@user_app.get('/{user_id}', response_model=UserResponse)
def get_users_by_id(user_id: int):
    with Session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            return UserResponse.model_dump(user)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )


@user_app.patch('/{user_id}')
def put_user(user_id: int, user_data: UserPatchUpdate):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            update_data = user_data.model_dump(exclude_unset=True)
            session.merge(User(id=user_id, **update_data))
            return {'status': 'patch updated'}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )


@user_app.delete('/{user_id}')
def delete_user(user_id: int):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            session.delete(user)
            return {'status': 'deleted'}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
