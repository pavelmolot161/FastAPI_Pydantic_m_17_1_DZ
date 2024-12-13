
### - 13.12.24

from fastapi import APIRouter, Depends, status, HTTPException

           # Сессия БД
from sqlalchemy.orm import Session

           # Функция подключения к БД
from app.backend.db_depends import get_db

           # Аннотации, Модели БД и Pydantic.
from typing import Annotated, List, Union
from app.models import Task
from app.models import User
from app.schemas.user import CreateUser, UpdateUser
from app.schemas.task import CreateTask, UpdateTask

           # Функции работы с записями.
from sqlalchemy import insert, select, update, delete
           # Функция создания slug-строки
from slugify import slugify

router = APIRouter(
    prefix="/task",
    tags=["task"]
)

#______________________________________________________________________________________________________
@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

#_____________________________________________________________________________________________________

@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()    ### - Извлечение пользователя по ID
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found (1)")             ### - Исключение, если пользователь не найден
    return task

#_____________________________________________________________________________________________________

@router.post("/create", response_model=Union[CreateTask, None, bool])
async def create_task(
    db: Annotated[Session, Depends(get_db)],
    create_task: CreateTask,
    user_id: int                                                          ### - Добавлено: параметр user_id
):
    slug = slugify(create_task.title)
                                                                          ### - Проверка на существование пользователя
    existing_user = db.execute(select(User).where(User.id == user_id)).fetchone()

    if not existing_user:                                                 ### - Если пользователь не найден
        raise HTTPException(status_code=404, detail="Task was not found (2)")     ### - Исключение 404

    existing_task = db.execute(select(Task).where(Task.slug == slug)).fetchone()  ### - Проверка на существующий slug
    if existing_task:
        ### - Возвращаем сообщение об ошибке, если slug уже существует
        raise HTTPException(status_code=400, detail="Slug already exists (3)")

    new_task = Task(
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority,
        slug=slug,
        user_id=user_id                    ### - Добавлено: связываем задачу с пользователем
    )
    db.add(new_task)
    db.commit()
    return new_task                        ### - Возвращаем созданную задачу, которая соответствует модели CreateTask

#_________________________________________________________________________________________

@router.put("/update", response_model=UpdateTask)
async def update_task(
        db: Annotated[Session, Depends(get_db)],
        id: int,
        task_data: UpdateTask              ### -  Добавлен параметр для получения данных обновления
):
    task = db.scalars(select(Task).where(Task.id == id)).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found (4)"
        )

    ### - Обновление пользователя значениями из модели UpdateTask
    db.execute(update(Task).where(Task.id == id).values(
        title=task_data.title,
        content=task_data.content,
        priority=task_data.priority
    ))
    db.commit()

    # return {                                                   ### - КАК ЕГО ЗАПУСТИТЬ   --- ???
    #     'status_code': status.HTTP_200_OK,
    #     'transaction': "User update is successful (4)!"
    # }

    ### - Возвращаем обновленнst данные
    return {
        'title': task.title,
        'content': task_data.content,
        'priority': task_data.priority
    }

#______________________________________________________________________________

@router.delete("/delete")
async def delete_task(id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found (5)"
        )

    db.delete(task)                                                ### - Удаление данных
    db.commit()
    return task

### - ___________________________________________________________________________________________________________
