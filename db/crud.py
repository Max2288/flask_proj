from http import HTTPStatus
from http.client import HTTPException

import sqlalchemy
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
        db_session.rollback()  # Откатываем транзакцию в случае ошибки.
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.args)
    return {"message": 'Пользователь создан'}

