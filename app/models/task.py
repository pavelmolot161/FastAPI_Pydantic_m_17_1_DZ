### - 2,3,4 занятие
from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models import *

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)            ### - по умолчанию 0
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)   ### - уникальная строка с индексом
    user = relationship('User', back_populates='tasks')  ### - объект связи с таблицей User
                                                                   ## связывает сущности между собой 1 - 1

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
