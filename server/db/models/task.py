from typing import List, Literal
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey

from .. import Base
# no-active , 
class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[Literal['not_started', 'in_progress', 'in_review', 'done']] = mapped_column(default='not_started')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='tasks', uselist=False)