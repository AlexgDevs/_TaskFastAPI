from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash


engine = create_engine(
    url='sqlite:///treker.db',
    echo=True
)


Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def up():
    Base.metadata.create_all(engine)


def drop():
    Base.metadata.drop_all(engine)


def migrate():
    drop()
    up()


from .models import (
    User,
    Task,
    Project
)