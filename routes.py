from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required, user_unauthorized
from ModelsDataBase import *
from Classes import *
from __init__ import db, admin, app
import views


@app.route('/')
def main_page():
    return render_template('index.html', construction_positions=get_available_building())


# @app.route('/admin', methods=['GET', "POST"])
# def admin_page():
#     if current_user.role > 0:
#         return render_template('admin.html')
#     flash('У вас нет прав на данную страницу!')
#     return render_template('index.html')

@app.route('/single_build/<id>')
def build_single(id):
    flats = get_available_flat_in_construction_position(id)
    return render_template('building_single.html', flats=flats, construction=get_construction_by_position(id),
                           construction_position=get_construction_position(id))


# @app.route('/single_build/<id>/flat/<flat_id>', methods=['GET', "POST"])
# def get_flat_by_id(id, flat_id):
#     return render_template('building_single.html')
#
#
# @app.route('admins/input_construction', methods=['GET', "POST"])
# def input_construction():
#     return render_template('index.html', type_building=get_type_building())


@app.route('/signup', methods=['GET', "POST"])  # регистрация
def signup():
    if request.method == 'POST':
        email = request.form.get('inputEmail')
        password = generate_password_hash(
            request.form.get('inputPassword'))  # генерируем пароль для сохранения в базу данных
        if email and password:
            # new_user = Human(full_name=nameUser, email=email, phone=phone,
            #                  password_hash=password, privelege=0)#создаем нового пользователя и добавляем в базу данных
            db.engine.execute(
                f'INSERT INTO user_site (email,password_hash) VALUES (%s,%s)',  # добавляем нового юзера
                (email, password,))  # добавляем нового пользователя
            return render_template('index.html')
    return render_template('signup.html')


@app.route('/signin', methods=['GET', "POST"])  # Вход пользователя
def login_page():
    # form  = LoginForm()
    login = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    # берем данные с формы
    if request.method == 'POST':  # Данные с формы отправляются только в post запросе
        user = UserSite.query.filter_by(
            email=login).first()  # Берем из базы данных пользователя, он будет объект описанный в классе models, фактически это запрос (select * from human where email = login)
        if user == None:
            return redirect('signup')
        if user.check_password(password):  # сверяем hash пароля и пароль введенный на сайте
            login_user(user)  # запоминаем пользователя
            return redirect('admin')
        else:
            flash('Проверьте правильность логина и пароля')

    return render_template('SignIn.html')


@app.route("/logout")  # выход пользователя из браузера
def logout_page():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()
