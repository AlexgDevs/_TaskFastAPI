from flask_wtf import FlaskForm
from sqlalchemy import select
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, ValidationError, validators
from wtforms.validators import Length, EqualTo, DataRequired
from werkzeug.security import check_password_hash

from ..db import Session, User, Project


class ProjectForm(FlaskForm):
    title = StringField('Название проекта', validators=[
        DataRequired(message='Обязательное поле'),
        Length(max=50, message='Максимальное колличество символов - 50')
    ])

    description = StringField('Описание', validators=[
        DataRequired(message='Обязательное поле'),
        Length(max=512, message='Максимальное колличество символов - 512')
    ]
    )

    submit = SubmitField('Создать')

    def validate_title(self, field):
        with Session() as session:
            project = session.scalar(select(Project).where(Project.title == field.data, Project.user_id == current_user.id))
            if project:
                raise ValidationError('Такое название проекта уже есть')
            return field.data


class ProjectPactchForm(FlaskForm):
    title = StringField('Название', validators=[
        Length(max=50)
    ])

    description = StringField('Описание', validators=[
        Length(max=512)
    ])

    submit = SubmitField('Изменить')