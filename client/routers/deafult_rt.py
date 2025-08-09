from collections import defaultdict
from flask import render_template, request
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import requests

from .. import app, API_URL
from ..db import Session, Task, User, Project


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


@app.get('/tasks/lists')
@login_required
def tasks_lists():
    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        response = requests.get(f'{API_URL}/projects/{current_user.id}')
        projects =  response.json()

    return render_template('list_tasks.html', current_user=current_user, user=user, projects=projects)
