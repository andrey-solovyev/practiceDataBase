from flask import Flask, render_template, request, redirect, flash
from flask_login import *
from __init__ import *
from ModelsDataBase import *
from Classes import *

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('admin', methods=['GET', "POST"])
@user_unauthorized
def admin():
    if current_user.role > 0:
        return render_template('admin.html')
    flash('У вас нет прав на данную страницу!')
    return render_template('index.html')


@app.route('/signin', methods=['GET', "POST"])  # Вход пользователя
def login():
    # form  = LoginForm()
    login = request.form.get('inputLogin')
    password = request.form.get('inputPassword')
    # берем данные с формы
    if request.method == 'POST':  # Данные с формы отправляются только в post запросе
        user = User_Site.query.filter_by(
            email=login).first()  # Берем из базы данных пользователя, он будет объект описанный в классе models, фактически это запрос (select * from human where email = login)

        if user.check_password(password):  # сверяем hash пароля и пароль введенный на сайте
            login_user(user)  # запоминаем пользователя
            return redirect('admin')
        else:
            flash('Проверьте правильность логина и пароля')

    return render_template('SignIn.html')


@app.route("/logout")  # выход пользователя из браузера
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()
