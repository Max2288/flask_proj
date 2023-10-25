import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Класс, содержащий настройки приложения.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Флаг отслеживания изменений SQLAlchemy.
        TEMPLATES_AUTO_RELOAD (bool): Флаг автоматической перезагрузки шаблонов.
        TEMPLATE_FOLDER (str): Путь к папке с шаблонами.
        SECRET_KEY (str): Секретный ключ для приложения.
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
        os.environ["PG_USER"],
        os.environ["PG_PASSWORD"],
        os.environ["PG_HOST"],
        os.environ["DB_NAME"]
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    TEMPLATE_FOLDER = os.environ["TEMPLATE_FOLDER"]
    SECRET_KEY = os.environ["SECRET_KEY"]


class UserConfig:
    """
    Класс, содержащий настройки пользователя.

    Attributes:
        SENDER (str): Email-адрес отправителя.
        PASSWORD_SENDER (str): Пароль отправителя.
        DOMAIN (str): Домен для настройки SMTP-сервера.
        PORT (str): Порт для настройки SMTP-сервера.
        SCHEMA_NAME (str): Имя схемы базы данных.
    """
    SENDER = os.environ["SENDER"]
    PASSWORD_SENDER = os.environ["PASSWORD_SENDER"]
    DOMAIN = os.environ["DOMAIN"]
    PORT = os.environ["PORT"]
    SCHEMA_NAME = os.environ["SCHEMA_NAME"]
