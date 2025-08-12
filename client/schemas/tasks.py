from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, DateTimeField, ValidationError, validators, FileField
from wtforms.validators import Length, EqualTo, DataRequired
from werkzeug.utils import secure_filename
from base64 import b64encode

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
        'Дедлайн задачи. Формат ГГГГ.ММ.ДД',
        format='%Y.%m.%d',
        validators=[
            DataRequired(message='Поле обязательное'),
        ]
    )

    photo = FileField('Прикрепите фотографию', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Допустимые форматы: jpg, png, jpeg')
    ])

    submit = SubmitField('Создать')

    def validate_dead_line(self, field):
        if not isinstance(field.data, datetime):
            raise ValidationError('Неверный формат данных')

        if field.data < datetime.now():
            raise ValidationError('Дедлайн должен быть в будущем')
        return field.data



class TaskPatchForm(FlaskForm):
    title = StringField('Название', validators=[
        Length(max=150)
    ])

    description = StringField('Описание', validators=[
        Length(max=2048)
    ])

    submit = SubmitField('Изменить')
