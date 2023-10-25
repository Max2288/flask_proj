from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    """
    Форма для входа пользователя.

    Attributes:
        username (StringField): Поле для ввода логина.
        password (PasswordField): Поле для ввода пароля.
        submit (SubmitField): Кнопка для отправки формы.
    """
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    """
    Форма для регистрации пользователя.

    Attributes:
        username (StringField): Поле для ввода логина.
        password (PasswordField): Поле для ввода пароля.
        submit (SubmitField): Кнопка для отправки формы.
    """
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class FeedbackForm(FlaskForm):
    """
    Форма для отправки обратной связи.

    Attributes:
        email (StringField): Поле для ввода почтового адреса.
        message (TextAreaField): Поле для ввода текста сообщения.
        submit (SubmitField): Кнопка для отправки формы.
    """
    email = StringField('Ваша почта', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить сообщение')
