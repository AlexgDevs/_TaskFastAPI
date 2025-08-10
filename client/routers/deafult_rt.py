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
def show_status_dashboard():
    '''Показывает страницу где находятся задачи отсортированные по статусам'''
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
            'status_dashboard.html',
            sorted_tasks=sorted_tasks,
            user=user
        )