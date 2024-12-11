
from .user import User
from .task import Task
from app.backend.db import Base, engine   ### - добавлено 11.12.24

Base.metadata.create_all(engine)          ### - добавлено 11.12.24