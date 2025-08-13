from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import requests
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from ..schemas import RegisterForm, LoginForm, ChangeProfileForm, VerificationCodeForm
from ..utils import (
    LoginUser,
    admin_requried,
    required_not_authenticated,
    create_verifi_code,
    send_verification_code,
    smtp_server,
    smtp_port,
    from_email,
    pwd
    )

from ..db import Session, User
from .. import app, API_URL

@app.get('/auth/register')
@required_not_authenticated
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.get('/auth/login')
@required_not_authenticated
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.post('/auth/register')
@required_not_authenticated
def register():
    form = RegisterForm()
    ver_form = VerificationCodeForm()
    if form.validate_on_submit():
        with Session.begin() as session:

            code = create_verifi_code()

            new_user = User(
                name=form.name.data,
                password=generate_password_hash(form.password.data),
                email=form.email.data,
                verifi_code=code['code']
            )

            session.add(new_user)
            session.flush()

            send_verification_code(from_email, new_user.email, smtp_server, smtp_port, pwd, code['code'])
            return render_template('email_verification.html', ver_form=ver_form, exp=code['exp'], user_id=new_user.id)

    else:
        return render_template('register.html', form=form)


@app.post('/send/verification_code')
def check_code():
    ver_form = VerificationCodeForm()
    if ver_form.validate_on_submit():
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.id == int(request.form.get('user_id'))))
            if user:

                if user.verifi_code != ver_form.code.data:
                    flash('Неверный код', 'error')
                    return render_template('email_verification.html', ver_form=ver_form)
                
                if datetime.fromisoformat(request.form.get('code_exp')) < datetime.now():
                    flash('Время работы кода истекло!', 'error')
                    session.delete(user) #можно на фастапи перенести
                    return redirect(url_for('register_page'))

                login_user(LoginUser(id=user.id, name=user.name, role=user.role))
                flash('Успешно авторизовались', 'info')
                user.verifi_code = None
                return redirect(url_for('show_status_dashboard'))
    
    return render_template('email_verification.html', ver_form=ver_form, exp=request.form.get('exp'), user_id=request.form.get('user_id'))


@app.post('/auth/login')
@required_not_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.scalar(select(User).where(User.name == form.name.data))
            if user:
                login_user(LoginUser(id=user.id, name=user.name, role=user.role))
                flash('Вы успешно вошли в аккаунт!', 'info')
                return redirect(url_for('show_status_dashboard'))
    else:
        return render_template('login.html', form=form)


@app.get('/auth/logout')
@login_required
def logout_page():
    return render_template('logout.html')


@app.get('/auth/logout/accept')
@login_required
def logout_accept():
    logout_user()
    return redirect(url_for('login_page'))


@app.get('/auth/logout/cancel')
@login_required
def logout_cancel():
    return redirect(url_for('show_status_dashboard'))


@app.get('/auth/profile/change-page')
@login_required
def change_profile_page():
    return redirect(url_for('show_profile'))


@app.post('/auth/profile/change')
@login_required
def change_profile():
    form = ChangeProfileForm()
    if form.validate_on_submit():

        data = {
            'name': form.name.data,
        }

        response = requests.patch(f'{API_URL}/users/{current_user.id}', json=data)

        flash('Успешно обновлено', 'info')
        return redirect(url_for('show_profile'))
    
    flash('Неверное имя или пароль', 'error')
    return redirect(url_for('show_profile', form=form))