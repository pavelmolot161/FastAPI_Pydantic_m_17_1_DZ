
### - FastAPI_Pydantic_m_17_1_DZ
### - 26.11.24
### - Установка - >>> pip install uvicorn
### - Переход в cd app вот так - (.venv) PS D:\FastAPI_Pydantic_m_17> >>> cd app
### - ЗАПУСК - >>> python -m uvicorn module_17_1_DZ:app

from fastapi import FastAPI
from routers import task, user

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)