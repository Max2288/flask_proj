import smtplib

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from loguru import logger
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from common.utils import (generate_token, send_email_message, smtp_generator,
                          token_required)
from config import Config, UserConfig
from db.crud import create_user
from db.models import Cheese, User
from db.session import get_db
from forms import *

app = Flask('cheese_shop')
app.config.from_object(Config)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Функция загрузки пользователя для Flask-Login.

    Args:
        user_id: Идентификатор пользователя.

    Returns:
        User: Объект пользователя, если найден в базе данных, иначе None.
    """
    db = next(get_db())
    return db.query(User).get(user_id)


@app.route('/')
def index():
    """
    Обработчик маршрута '/' (главная страница).

    Returns:
        str: HTML-шаблон для главной страницы.
    """
    db = next(get_db())
    cheese = db.query(Cheese).all()
    return render_template('index.html', cheese=cheese)


@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Обработчик маршрута '/profile' (профиль пользователя).

    Returns:
        str: HTML-шаблон для страницы профиля пользователя.
    """
    form = FeedbackForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        try:
            with smtp_generator(
                smtplib.SMTP(
                    "smtp.{0}".format(UserConfig.DOMAIN),
                    UserConfig.PORT
                )
            ) as email_server:
                send_email_message(email_server, current_user.username, email)
        except Exception as err:
            logger.error(
                "{0}\nПроверьте логин или пароль!".format(err)
            )
            flash(f'Произошла ошибка во время отправки! {err}', 'danger')
        else:
            flash('Сообщение успешно отправлено!', 'success')
    return render_template('profile.html', user=current_user, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login(db: Session = next(get_db())):
    """
    Обработчик маршрута '/login' (вход пользователя).

    Returns:
        str: HTML-шаблон для страницы входа.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = db.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            token = generate_token(user.id)
            session['token'] = token
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        flash('Вы не смогли войти! Проверьте ваши данные.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register(db: Session = next(get_db())):
    """
    Обработчик маршрута '/register' (регистрация пользователя).

    Returns:
        str: HTML-шаблон для страницы регистрации.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        create_user(db, user)
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Обработчик маршрута '/logout' (выход пользователя).

    Returns:
        str: HTML-шаблон для страницы выхода.
    """
    logout_user()
    session.pop('token', None)
    flash('Вы успешно вышли!', 'success')
    return redirect(url_for('index'))


@app.route('/cheese/api')
@token_required
def cheese_api():
    """
    Обработчик маршрута '/cheese/api' для получения данных о сырах в формате JSON.

    Returns:
        JSON: Данные о сырах в формате JSON.
    """
    db = next(get_db())
    cheeses = db.query(Cheese).all()
    cheese_data = [
        {
            "name": cheese.name,
            "description": cheese.description,
            "image_path": cheese.image_path
        }
        for cheese in cheeses
    ]
    return jsonify(cheese_data)


if __name__ == '__main__':
    app.run(debug=True)
