from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateTimeField, validators
from wtforms.validators import Length, EqualTo, DataRequired


class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[
        DataRequired(message='Обязательное поле'),
        Length(max=150, message='Максимальное колличество символов - 150')
    ])

    description = StringField('Описание', validators=[
        DataRequired(message='Обязательное поле'),
        Length(max=2048, message='Максимальное колличество символов - 2048')
    ]
    )

    dead_line = DateTimeField(
        'Дедлайн задачи',
        format='%Y.%m.%d',
    )

    submit = SubmitField('Создать')
