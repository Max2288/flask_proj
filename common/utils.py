import smtplib
from contextlib import contextmanager
from email.mime.text import MIMEText
from smtplib import SMTPResponseException, SMTPServerDisconnected

from loguru import logger

from config import UserConfig


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