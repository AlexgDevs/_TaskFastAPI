from collections import defaultdict
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import requests

from .. import app, API_URL
from ..db import Session, Task, User, Project
from ..schemas import ProjectForm


@app.get('/')
@login_required
def main():

    status = request.args.get('status')

    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        response = requests.get(
            f'{API_URL}/tasks/{user.id}', params={'status': status})

        tasks = response.json()

        sorted_tasks = {
            'not_started': [],
            'in_progress': [],
            'in_review': [],
            'burned_down': [],
            'done': []
        }

        for task in tasks:
            sorted_tasks[task['status']].append(task)

        return render_template(
            'main.html',
            sorted_tasks=sorted_tasks,
            user=user
        )


@app.get('/projects/list')
@login_required
def projects_list():
    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        response = requests.get(f'{API_URL}/projects/{current_user.id}')
        projects =  response.json()

    return render_template('projects_coulmns.html', current_user=current_user, user=user, projects=projects)

# перенесу в файл projects_rt

@app.get('/projects')
@login_required
def projects_page():
    form = ProjectForm()
    return render_template('create_project.html', form=form)


@app.post('/projects')
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'description': form.description.data,
            'user_id': current_user.id,
        }

        response = requests.post(f'{API_URL}/projects', json=data)
        if response.status_code == 201:
            flash('Проект успешно создан', 'info')
            return redirect(url_for('projects_list'))
        
        else:
            flash('Не удалось создать проект', 'error')
            return render_template('create_project.html', form=form)
    
    return render_template('create_project.html', form=form)
