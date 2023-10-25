from typing import Generator

import sqlalchemy.engine
from sqlalchemy.orm import sessionmaker

from config import Config

# Создаем SQLAlchemy механизм и устанавливаем соединение с базой данных
engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

def get_db() -> Generator:
    """
    Создает и предоставляет сессию базы данных как контекстный ресурс.

    Yields:
        sqlalchemy.orm.Session: Сессия базы данных, предоставляемая как контекстный ресурс.

    Notes:
        Эта функция создает новую сессию базы данных с использованием фабрики сессий SessionLocal,
        предоставляет ее как контекстный ресурс с помощью yield, и автоматически закрывает сессию после завершения
        блока контекста (в блоке `finally`). Это гарантирует корректное управление сессией и предотвращение
        утечек ресурсов.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
