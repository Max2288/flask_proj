import uuid
from typing import Any

import flask_login
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from config import UserConfig

# Определение метаданных для таблиц
metadata = sa.MetaData(
    schema=UserConfig.SCHEMA_NAME,
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

# Создание базового класса для всех сущностей базы данных
Base: Any = declarative_base(metadata=metadata)

class UUIDMixin:
    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

class User(flask_login.UserMixin, Base, UUIDMixin):
    """
    Модель пользователя, представляющая информацию о пользователе в базе данных.

    Attributes:
        username (str): Уникальное имя пользователя.
        password (str): Хэшированный пароль пользователя.
        is_admin (bool): Флаг, указывающий, является ли пользователь администратором.
    """
    __tablename__ = "user"

    username = sa.Column(sa.String(80), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    is_admin = sa.Column(sa.Boolean, default=False)

class Cheese(Base, UUIDMixin):
    """
    Модель сыра, представляющая информацию о различных сортах сыра.

    Attributes:
        name (str): Название сорта сыра.
        description (str): Описание сорта сыра.
        image_path (str): Путь к изображению сыра.
    """
    __tablename__ = "cheese"

    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text)
    image_path = sa.Column(sa.String(255))
