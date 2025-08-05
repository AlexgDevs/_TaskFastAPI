from typing import List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime

from .. import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(255))
    joined: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='user', cascade='all, delete-orphan')