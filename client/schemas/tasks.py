from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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

    submit = SubmitField('Создать')