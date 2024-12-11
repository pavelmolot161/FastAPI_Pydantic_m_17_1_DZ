### - перемещена инфа в папку арр - 11.12.24

### - организация запуска из папки арр файла __init__
#                                         1) - (.venv) PS D:\FastAPI_Pydantic_m_17> >>> pip install fastapi[standard]
### - ЗАПУСК когда файл (__init__) в директории арр (для поиска файла фастапи) = арр
#                                         2) - (.venv) PS D:\FastAPI_Pydantic_m_17> >>> fastapi dev app

### - FastAPI_Pydantic_m_17_1_DZ
### - 09.11.24
### - Установка - >>> pip install uvicorn
### - Переход в cd app вот так - (.venv) PS D:\FastAPI_Pydantic_m_17> >>> cd app
### - Выход на один путь назад - (.venv) PS D:\FastAPI_Pydantic_m_17\app> >>> cd ../
### - ЗАПУСК - >>> python -m uvicorn module_17_1_DZ:app
### - >>> uvicorn app.module_17_1:app --reload                               ### - если запускной файл в app
### - ЗАПУСК - >>> python -m uvicorn __init__:app
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

### - (.venv) PS D:\FastAPI_Pydantic_m_17> - >>> alembic revision --autogenerate -m "Initial migration Первоначальная миграция" ###
### - (.venv) PS D:\FastAPI_Pydantic_m_17> - >>> alembic upgrade head ### - Alembic проверяет текущую версию схемы базы
                                                    ## данных и применяет все миграции, которые ещё не были применены,
                                                    # до самой последней версии. Это позволяет Вам
                                                    # поддерживать базу данных в актуальном состоянии с
                                                    # последними изменениями схемы.


from fastapi import FastAPI
from app.routers import task, user
import app.models


fastapi_app = FastAPI()


@fastapi_app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager (1)"}

fastapi_app.include_router(task.router)    ### - активирует в FastAPI Swagger - router запросы task
fastapi_app.include_router(user.router)    ### - активирует в FastAPI Swagger - router запросы user

#_________________________________________________________________________________________

### - Справочный материал:...


# target_metadata = None   ### - было..
# from app.backend.db import Base
# from app.models.task import Task
# from app.models.user import User
# target_metadata = Base.metadata


# sqlalchemy.url = driver://user:pass@localhost/dbname   ### - было
# sqlalchemy.url = sqlite:///taskmanager.db
