from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import requests
from sqlalchemy import select
from base64 import b64encode

from ..schemas import TaskForm, TaskPatchForm
from .. import app, API_URL
from ..db import Session, Task


@app.get('/tasks/create/page')
@login_required
def create_task_page():
    '''Страница для создания задачи'''
    form = TaskForm()
    project_id = request.args.get('project_id')
    return render_template('create_task.html', form=form, project_id_rd=project_id)


@app.post('/tasks/create')
@login_required
def create_task():
    '''Обработка страницы создания задачи'''
    form = TaskForm()
    if form.validate_on_submit():

        file = form.photo.data
        file.seek(0)
        file_bs64 = b64encode(file.read()).decode()

        data_form = {
            'title': form.title.data,
            'description': form.description.data,
            'dead_line': form.dead_line.data.strftime('%Y.%m.%d'),
            'user_id': current_user.id,
            'project_id': request.form.get('project_id'),
            'photo': file_bs64
        }

        response = requests.post(f'{API_URL}/tasks', json=data_form)
        if response.status_code == 201:
            flash('Вы успешно создали задачу!', 'info')
            return redirect(url_for('show_projects'))

        else:
            flash('Не удалось создать заметку. Попробуйте еще раз', 'error')
            return render_template('create_task.html', form=form)

    return render_template('create_task.html', form=form)


@app.post('/tasks/change_status')
@login_required
def change_status():
    '''Изменение статуса задачи'''
    status = request.form.get('status')
    task_id = request.form.get('task_id')

    data = {
        'status': status,
        'id': task_id
    }

    response = requests.patch(
        f'{API_URL}/tasks/{task_id}/{current_user.id}', json=data)

    flash('Статус обновлен', 'info')
    return redirect(url_for('show_status_dashboard'))


@app.post('/tasks/change/other_page')
@login_required
def task_change_other_page():
    form = TaskPatchForm()
    return render_template('change_task_other.html', form=form, project_id=request.form.get('task_id'))


@app.post('/tasks/change/other')
def task_change_other():
    form = TaskPatchForm()
    if form.validate_on_submit():
        task_id = request.form.get('project_id')

        data = {
            'title': form.title.data,
            'description': form.description.data,
        }

        response = requests.patch(f'{API_URL}/tasks/{task_id}/{current_user.id}', json=data)
        return redirect(url_for('show_status_dashboard'))