import requests

from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import select

from ..schemas import ProjectForm
from .. import app, API_URL
from ..db import Session, User, Project


@app.get('/projects')
@login_required
def show_projects():
    '''Страница где будут проекты пользователя,  а в них задачи'''
    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        response = requests.get(f'{API_URL}/projects/{current_user.id}')
        projects =  response.json()

    return render_template('projects_dashboard.html', current_user=current_user, user=user, projects=projects)


@app.get('/projects/create/page')
@login_required
def create_project_page():
    '''Страница где будет форма создания проекта'''
    form = ProjectForm()
    return render_template('create_project.html', form=form)


@app.post('/projects/create')
@login_required
def create_project():
    '''Обработка формы создания проекта'''
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
            return redirect(url_for('show_projects'))
        
        else:
            flash('Не удалось создать проект', 'error')
            return render_template('create_project.html', form=form)
    
    return render_template('create_project.html', form=form)
