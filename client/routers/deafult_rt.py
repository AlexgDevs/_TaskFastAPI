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
        pass