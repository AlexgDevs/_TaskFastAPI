from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from ..schemas import RegisterForm, LoginForm
from ..utils import LoginUser, admin_requried, required_not_authenticated
from ..db import Session, User
from .. import app

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
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.name == form.name.data))
            if user:
                flash('Имя пользователя занято', 'info')
                return render_template('register.html', form=form)

            new_user = User(
                name=form.name.data,
                password=generate_password_hash(form.password.data)
            )

            session.add(new_user)
            session.flush()

            login_user(LoginUser(
                id=new_user.id,
                name=new_user.name,
                role=new_user.role))

            flash('Вы успешно авторизовались', 'info')
            return redirect(url_for('main'))

    else:
        return render_template('register.html', form=form)


@app.post('/auth/login')
@required_not_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            user = session.scalar(select(User).where(User.name == form.name.data))
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(LoginUser(id=user.id, name=user.name, role=user.role))
                    flash('Вы успешно вошли в аккаунт!', 'info')
                    return redirect(url_for('main'))
                else:
                    flash('Неверный логин или пароль', 'info')
                    return render_template('login.html', form=form)
            else:
                flash('Имя пользователя не найдено', 'info')
                return render_template('login.html', form=form)

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
    return redirect(url_for('main'))
