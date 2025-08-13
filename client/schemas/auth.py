from flask_wtf import FlaskForm
from sqlalchemy import select
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, ValidationError, validators, EmailField
from wtforms.validators import Length, EqualTo, DataRequired
from werkzeug.security import check_password_hash

from ..db import Session, User


class RegisterForm(FlaskForm):
    name = StringField(
        'Имя', validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=150, message='Максимальное кол-во символов -- 150'),
        ],
    )

    email = EmailField('Почта', validators=[
        DataRequired('Обязательное поле')
    ])

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

    def validate_name(self, field):
        with Session() as session:
            user = session.scalar(select(User).where(User.name == field.data))
            if user:
                raise ValidationError('Имя пользователя уже существует')

            return field.data


class VerificationCodeForm(FlaskForm):
    code = StringField('Код поддтверждения', validators=[
        DataRequired('Обязательное поле'),
        Length(min=6, max=6, message='Код из 6 цифр')
    ])

    submit = SubmitField('Отправить')


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

    def validate_name(self, field):
        with Session() as session:
            user = session.scalar(select(User).where(User.name == field.data))
            if not user:
                raise ValidationError('Пользователь не найден')

            return field.data

    def validate_password(self, field):
        with Session() as session:
            user = session.scalar(select(User).where(
                User.name == self.name.data))
            if user:
                if not check_password_hash(user.password, field.data):
                    raise ValidationError('Неверный пароль')


class ChangeProfileForm(FlaskForm):
    last_name = StringField('Текущее имя', validators=[
        Length(max=150, message='Максимальное кол-во символов -- 150')
    ])

    name = StringField(
        'Новое имя',
        validators=[
            Length(max=150, message='Максимальное кол-во символов -- 150')
        ]
    )

    # почта будет потом

    password = PasswordField(
        'Пароль для действия',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длинна пароля - 8')
        ]
    )

    # cooming soon...

    submit = SubmitField('Изменить')

    def validate_last_name(self, field):
        with Session() as session:
            user = session.scalar(select(User).where(User.name == field.data))
            if not user:
                raise ValidationError('Некорректное имя')
            return field.data

    def validate_password(self, field):
        with Session() as session:
            user = session.scalar(select(User).where(
                User.name == self.last_name.data))
            if user:
                if not check_password_hash(user.password, field.data):
                    raise ValidationError('Неверный пароль для текущего имени')
                return field.data
