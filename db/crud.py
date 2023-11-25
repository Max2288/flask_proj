from http import HTTPStatus
from http.client import HTTPException

import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from db.models import Cheese, User


def create_user(db_session: Session, user: User):
    """
    Создает нового пользователя в базе данных.

    Args:
        db_session (Session): Сессия базы данных, в которой будет создан пользователь.
        user (User): Объект пользователя, который будет создан.

    Raises:
        HTTPException: Исключение, которое может быть вызвано в случае конфликта при создании пользователя.

    Returns:
        dict: Словарь с сообщением о создании пользователя.

    Notes:
        Если возникает исключение IntegrityError во время создания пользователя, 
        то сессия db_session будет откатываться до начального состояния перед вызовом этой функции. 
        Это предотвращает несогласованное состояние базы данных после ошибки.
    """
    try:
        db_session.add(
            User(
                username=user.username,
                password=generate_password_hash(user.password)
            )
        )
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        db_session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(exc.orig)
        )
    return {"message": 'Пользователь создан'}


def create_cheese(db_session: Session, name: str, description: str, image_path: str):
    """
    Создает или обновляет запись о сыре в базе данных.

    Args:
        db_session (Session): Сессия базы данных.
        name (str): Название сыра.
        description (str): Описание сыра.
        image_path (str): Путь к изображению сыра.

    Returns:
        dict: Словарь с сообщением о создании или обновлении записи о сыре.
    """
    try:
        insert_stmt = insert(Cheese).values(
            name=name,
            description=description,
            image_path=image_path
        )

        on_conflict_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['name', 'description'],
            set_=dict(
                name=insert_stmt.excluded.name,
                description=insert_stmt.excluded.description,
                image_path=insert_stmt.excluded.image_path
            )
        )

        db_session.execute(on_conflict_stmt)
        db_session.commit()
        return {"message": "Запись о сыре создана или обновлена"}
    except IntegrityError as exc:
        db_session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(exc.orig)
        )
