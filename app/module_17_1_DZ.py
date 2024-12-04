
### - FastAPI_Pydantic_m_17_1_DZ
### - 30.11.24
### - Установка - >>> pip install uvicorn
### - Переход в cd app вот так - (.venv) PS D:\FastAPI_Pydantic_m_17> >>> cd app
### - ЗАПУСК - >>> python -m uvicorn module_17_1_DZ:app
### - (.venv) PS D:\FastAPI_Pydantic_m_17> - >>> pip install alembic
### - (.venv) PS D:\FastAPI_Pydantic_m_17> - >>> alembic init app/migrations ### - создание папки migrations.

'''После внесения дополнений в файлы:
    env.py:
            #target_metadata = None   ### - было

            from app.backend.db import Base
            from app.models.task import Task
            from app.models.user import User
            target_metadata = Base.metadata

    alembic.int:
            sqlalchemy.url = driver://user:pass@localhost/dbname   ### - было

            sqlalchemy.url = sqlite:///taskmanager.db
Запускаем через терминал автогенерацию. '''

### - (.venv) PS D:\FastAPI_Pydantic_m_17> - >>> alembic revision --autogenerate -m "Initial migration" - создание
                                                                                        ## миграции и файла с миграцией
### - (.venv) PS D:\FastAPI\FastAPI_Pydantic_m_17_DZ> - >>> alembic upgrade head -  применение последей миграции и
                                                    ## создание таблицы User, Task с записью текущей версии миграции:




from fastapi import FastAPI
from routers import task, user

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

#_________________________________________________________________________________________

### - Справочный материал:...


# target_metadata = None   ### - было..
# from app.backend.db import Base
# from app.models.task import Task
# from app.models.user import User
# target_metadata = Base.metadata


# sqlalchemy.url = driver://user:pass@localhost/dbname   ### - было
# sqlalchemy.url = sqlite:///taskmanager.db
