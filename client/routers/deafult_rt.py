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
        response = requests.get(f'{API_URL}/tasks').json()
        
        no_active_tasks = [task for task in response if task['status'] == 'no-active']
        in_process_tasks = [task for task in response if task['status'] == 'in_process']
        under_review_tasks = [task for task in response if task['status'] == 'under_review']
        done_tasks = [task for task in response if task['status'] == 'completed']


        return render_template(
            'main.html',
            current_user = current_user,
            user = user,
            no_active_tasks = no_active_tasks,
            in_process_tasks = in_process_tasks,
            under_review_tasks = under_review_tasks,
            done_tasks = done_tasks
        )