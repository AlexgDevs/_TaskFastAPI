from flask_wtf import FlaskForm
from sqlalchemy import select
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, ValidationError, validators
from wtforms.validators import Length, EqualTo, DataRequired
from werkzeug.security import check_password_hash

from ..db import Session, User


class RegisterForm(FlaskForm):
    name = StringField(
        'Имя', validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=150, message='Максимальное кол-во символов -- 150')
        ]
    )

    password = PasswordField(
        'Пароль', validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длинна пароля - 8')
        ]
    )

    password_confirm = PasswordField(
        'Повторите пароль', validators=[
            DataRequired(message='Обязательное поле'),
            EqualTo('password', message='Пароли не совпадают')
        ]
    )

    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    name = StringField(
        'Имя', validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=150, message='Максимальное кол-во символов -- 150')
        ]
    )

    password = PasswordField(
        'Пароль', validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длинна пароля - 8')
        ]
    )

    submit = SubmitField('Войти')


class ChangeProfileForm(FlaskForm):

    name = StringField(
        'Имя',
        validators=[
            Length(max=150, message='Максимальное кол-во символов -- 150')
        ]
    )

    password = PasswordField(
        'Пароль для действия',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длинна пароля - 8')
        ]
    )

    # cooming soon...

    submit = SubmitField('Изменить')
