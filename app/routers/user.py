
from fastapi import APIRouter, Depends, status, HTTPException

           # Сессия БД
from sqlalchemy.orm import Session

           # Функция подключения к БД
from app.backend.db_depends import get_db

           # Аннотации, Модели БД и Pydantic.
from typing import Annotated, List, Union
from app.models import User
from app.schemas.user import CreateUser, UpdateUser
from app.schemas.task import CreateTask, UpdateTask

           # Функции работы с записями.
from sqlalchemy import insert, select, update, delete
           # Функция создания slug-строки
from slugify import slugify

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

#_____________________________________________________________________________________________________________
@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()                     ### - Вставил all через жолтую лампочку
    return users
'''      Функция all_users: 
Изменена для использования db.scalars(select(User)).all(), что соответствует требованиям.'''
#_____________________________________________________________________________________________________________

@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).first()    ### - Извлечение пользователя по ID
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found (1)")             ### - Исключение, если пользователь не найден
    return user

'''      Функция user_by_id: 
Добавлена для извлечения пользователя по user_id. Если пользователь не найден, выбрасывается 
исключение с кодом 404 и соответствующим сообщением.'''
#_____________________________________________________________________________________________________________

@router.post("/", response_model=Union[CreateUser, None, bool])
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    slug = slugify(create_user.username)
    existing_user = db.execute(select(User).where(User.slug == slug)).fetchone()
    if existing_user:
        return {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'transaction': "Slug already exists (2)"
        }                                               ### - Возвращаем сообщение об ошибке, если slug уже существует

    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slug))
    db.commit()

    return create_user                                  ### - Возвращаем созданного пользователя

#_____________________________________________________________________________________________________________

@router.put("/update", response_model=UpdateUser)
async def update_user(
        db: Annotated[Session, Depends(get_db)],
        id: int,
        user_data: UpdateUser                           ### -  Добавлен параметр для получения данных обновления
):
    user = db.scalars(select(User).where(User.id == id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found (3)"
        )

    ### - Обновление пользователя значениями из модели UpdateUser
    db.execute(update(User).where(User.id == id).values(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age
    ))
    db.commit()

    # return {                                                   ### - КАК ЕГО ЗАПУСТИТЬ --- ???
    #     'status_code': status.HTTP_200_OK,
    #     'transaction': "User update is successful (4)!"
    # }

    ### - Возвращаем обновленного пользователя
    return {
        'username': user.username,
        'firstname': user_data.firstname,
        'lastname': user_data.lastname,
        'age': user_data.age
    }

#_____________________________________________________________________________________________________________

@router.delete("/delete")
async def delete_user(id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found (5)"
        )

    db.delete(user)                                              ### - Удаление пользователя
    db.commit()
    return user

###-________________________________________________________________________________________________________________
