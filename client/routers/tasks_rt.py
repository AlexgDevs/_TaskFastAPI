from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import requests
from sqlalchemy import select

from ..schemas import TaskForm
from .. import app, API_URL
from ..db import Session, Task


@app.get('/tasks')
@login_required
def task_page():
    form = TaskForm()
    return render_template('create_task.html', form=form)


@app.post('/tasks')
@login_required
def task():
    form = TaskForm()
    if form.validate_on_submit():

        data = {
            'title': form.title.data,
            'description': form.description.data,
            'dead_line': form.dead_line.data.strftime('%Y.%m.%d'),
            'user_id': current_user.id,
        }

        response = requests.post(f'{API_URL}/tasks', json=data)
        if response.status_code == 201:
            flash('Вы успешно создали задачу!', 'info')
            return redirect(url_for('main'))
        
        else:
            flash('Не удалось создать заметку. Попробуйте еще раз', 'error')
            return render_template('create_task.html', form=form)

    return render_template('create_task.html', form=form)


# ЗАВТРА НА ФАСТАПИ ПЕРЕПИШУ!!!!
@app.post('/tasks/change_status')
@login_required
def change_status():
    status = request.form.get('status')
    task_id = request.form.get('task_id')

    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == int(task_id), Task.user_id == current_user.id))
        if task:
            task.status = status
            flash('Статус обновлен', 'info')
            return redirect(url_for('main'))

        return redirect(url_for('main'))