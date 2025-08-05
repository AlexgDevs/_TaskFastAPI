from functools import wraps
from flask import redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user)
from sqlalchemy import select

from .. import app
from ..db import (
    Session,
    User)

app.secret_key = '123_test_123'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class LoginUser(UserMixin):
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


@login_manager.user_loader
def load_user(user_id: int):
    with Session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            return LoginUser(
                id=user.id,
                name=user.name,
                role=user.role
            )

    return None


def admin_requried(f):
    @wraps(f)
    def wrapper(*arg, **kwarg):
        if not current_user.is_authenticated or \
            not current_user.role == 'admin':
            return redirect(url_for('main'))
        return f(*arg, **kwarg)
    return wrapper


def required_not_authenticated(f):
    @wraps(f)
    def wrapper(*arg, **kwarg):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        return f(*arg, **kwarg)
    return wrapper


