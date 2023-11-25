import datetime
import json
import smtplib
from contextlib import contextmanager
from email.mime.text import MIMEText
from functools import wraps
from smtplib import SMTPResponseException, SMTPServerDisconnected
from typing import Any, Callable

from flask import make_response, session
from jwt import ExpiredSignatureError, PyJWT
from loguru import logger

from config import Config, UserConfig


@contextmanager
def smtp_generator(smtp: smtplib.SMTP):
    """
    Контекстный менеджер для работы с SMTP-сервером.

    Args:
        smtp (smtplib.SMTP): Объект SMTP-сервера.

    Yields:
        smtplib.SMTP: Объект SMTP-сервера, предоставленный как контекстный ресурс.

    Raises:
        SMTPResponseException: Исключение, которое может возникнуть при получении ответа с неправильным кодом от SMTP-сервера.
        SMTPServerDisconnected: Исключение, которое может возникнуть при разрыве соединения с SMTP-сервером.

    Notes:
        Этот контекстный менеджер предоставляет доступ к объекту SMTP-сервера и 
        автоматически завершает его работу после выхода из контекста.
        В случае разрыва соединения или некорректного ответа от сервера, произойдет соответствующая обработка исключений.
    """
    try:
        yield smtp
    finally:
        try:
            code, message = smtp.docmd("QUIT")
            if code != 221:
                raise SMTPResponseException(code, message)
        except SMTPServerDisconnected:
            pass
        finally:
            smtp.close()


def send_email_message(email_server: smtplib.SMTP, username: str, user_email: str):
    """
    Отправляет email-сообщение через SMTP-сервер.

    Args:
        email_server (smtplib.SMTP): Объект SMTP-сервера, через который будет отправлено сообщение.
        username (str): Имя пользователя, которому отправляется сообщение.
        user_email (str): Email-адрес получателя.

    Returns:
        None

    Notes:
        Эта функция устанавливает безопасное TLS-соединение, аутентифицируется на SMTP-сервере,
        формирует и отправляет email-сообщение с указанными параметрами. После успешной отправки
        сообщения, будет зарегистрировано информационное сообщение в логах.
    """
    email_server.starttls()
    email_server.login(UserConfig.SENDER, UserConfig.PASSWORD_SENDER)
    msg = MIMEText(
        f'Дорогой {username}, спасибо за предоставленную обратную связь,\
              в ближашее время постараемся ответить на твое обращение'
    )
    msg["Subject"] = 'Обратная связь'
    email_server.sendmail(UserConfig.SENDER, user_email, msg.as_string())
    logger.info(f"Сообщение для {user_email} было доставлено!")


def generate_token(user_id: Any) -> str:
    """
    Генерирует JWT токен для пользователя.

    Args:
        user_id (Any): Уникальный идентификатор пользователя.

    Returns:
        str: Сгенерированный JWT токен.
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id)
    }
    jwt_instance = PyJWT()
    return jwt_instance.encode(
        payload,
        Config.SECRET_KEY,
        algorithm='HS256'
    )


def token_required(f: Callable) -> Callable:
    """
    Декоратор для проверки JWT токена в сессии пользователя.

    Args:
        f (Callable): Функция, к которой применяется декоратор.

    Returns:
        Callable: Обернутая функция с проверкой токена.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token')
        if not token:
            response = json.dumps(
                {
                    'message': 'Отсутствует токен!'
                },
                ensure_ascii=False
            )
            return make_response(response, 401, {"Content-Type": "application/json"})
        try:
            jwt_instance = PyJWT()
            jwt_instance.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            response = json.dumps(
                {
                    'message': 'Токен просрочен!'
                },
                ensure_ascii=False
            )
            return make_response(response, 401, {"Content-Type": "application/json"})
        except:
            response = json.dumps(
                {
                    'message': 'Недействительный токен!'
                },
                ensure_ascii=False
            )
            return make_response(response, 401, {"Content-Type": "application/json"})
        return f(*args, **kwargs)
    return decorated_function
