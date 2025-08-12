from io import BytesIO
import base64
import numpy as np
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import matplotlib.pyplot as plt
from matplotlib import use
import requests

from .. import app, API_URL
from ..db import Session, Task, User, Project
from ..schemas import ProjectForm, ChangeProfileForm


use('agg')

# ПЕРЕНЕСТИ У ТИЛИТЫ ПОТОМ Щ:)
def generate_chart(diagram_data: dict):

    if not diagram_data or all(v == 0 for v in diagram_data.values()):
        diagram_data = {
            'Нет данных': 1
        }


    fig, ax = plt.subplots(figsize=(6, 6)) # создаем кароче наш плот fig - основное место где создается ax - это кароче наша диаграмма 6.6 это наши дюймы чтобы не плющилось
    ax.pie( # это кароче мы создаем круговую диаграмму
        diagram_data.values(), # наши значения
        labels=diagram_data.keys(), # это приписи к ним
        autopct='%1.1f%%', # это отступ после запятых
        colors=['#4CC9F0', '#4361EE', '#F8961E', '#F94144'], # цвета секторов
        startangle=90 # начало отсчета значений
    )
    ax.axis('equal') # делаем именно круг 

    buffer = BytesIO() # читаем байты
    plt.savefig(buffer, format='png', transparent=True) # сохраняем нашу диаграмму в бпйты в оперативку в виде png с прозрачным фоном
    buffer.seek(0) # возврощаемся в начало байтов
    chart_image = base64.b64encode(buffer.read()).decode() # декодируем наши байты
    plt.close(fig) # закрываем ткинтер чтобы не выебывался

    return chart_image


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
            user=user,
            total_done_tasks=len(sorted_tasks.get('done'))
        )


@app.get('/profile')
@login_required
def show_profile():
    form = ChangeProfileForm()
    with Session() as session:
        user = session.scalars(select(User).where(User.id == current_user.id)
                            .options(joinedload(User.tasks), joinedload(User.projects))).first()

        response = requests.get(
            f'{API_URL}/tasks/{user.id}')

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

        diagram_data = {
            'НН': len(sorted_tasks.get('not_started')),
            'ВП': len(sorted_tasks.get('in_progress')),
            'НП': len(sorted_tasks.get('in_review')),
            'СГ': len(sorted_tasks.get('burned_down')),
            'ГТ': len(sorted_tasks.get('done'))
        }

        chart_image = generate_chart(diagram_data)


    # EASY MATHPOTLIB :__) 

    return render_template('profile_settings.html', user=user, form=form, chart_image=chart_image)


@app.get('/users')
@login_required
def get_all_users():
    response = requests.get(f'{API_URL}/users', params={'role': 'user'})
    return response.json()


@app.get('/admins')
@login_required
def get_all_admins():
    response = requests.get(f'{API_URL}/users', params={'role': 'admin'})
    return response.json()