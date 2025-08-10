from typing import List, Literal
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey

from .. import Base

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='projects', uselist=False)

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='project', cascade='all, delete-orphan')