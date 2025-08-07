from collections import defaultdict
from flask import render_template, request
from flask_login import login_required, current_user
from sqlalchemy import select
import requests

from .. import app, API_URL
from ..db import Session, Task, User

@app.get('/')
@login_required
def main():
    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        response = requests.get(f'{API_URL}/tasks/{user.id}')

        tasks = response.json()

        sorted_tasks = {
            'not_started': [],
            'in_progress': [],
            'in_review': [],
            'done': []
        }

        for task in tasks:
            sorted_tasks[task['status']].append(task)
        

        return render_template(
            'main.html',
            sorted_tasks=sorted_tasks,
            user=user
        )