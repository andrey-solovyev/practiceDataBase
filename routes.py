import time

from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required, user_unauthorized
from ModelsDataBase import *
from Classes import *
from __init__ import db, admin, app
import views
from datetime import date, datetime


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
    flats = get_count_flats(id)
    return render_template('building_single.html', flats=flats, construction=get_construction_by_position(id),
                           construction_position=get_construction_position(id))


@app.route('/building')
def builidng_page():
    return render_template('blog.html', construction_positions=get_available_building())


@app.route('/menedger', methods=['GET', "POST"])
@login_required
def menedger_menu():
    return render_template('menedger.html', humans=get_all_humans())


@app.route('/search', methods=['GET', 'POST'])
def search_build():
    res = ""
    text = request.form.get('address')
    positions = get_construction_positions()
    for position in positions:
        print(position.address)
        if text in position.address:
            res += position.address
    return render_template('index.html', construction_positions=get_available_building(), res=res)

#  ПОИСК
@app.route('/search_perfomance', methods=['GET', 'POST'])
def search_perfomance():
    res = ""
    performances = None
    title = request.form.get('title')
    date_performance = request.form.get('date_performance')
    if date_performance == None:
        performances = get_performance_by_title(title)
    elif title != None and date_performance != None:
        performances = get_performance_by_title_and_date(title, date_performance.split()[0])
    return render_template('index.html', search_performances=performances)
#  КОНЕЦ ПОИСКа


@app.route('/menedger/add_himan', methods=["POST"])
@login_required
def menedger_add_human():
    if current_user.role > 0:
        # проверяем есть ли права админа имеет право только админ
        surname = request.form.get('surname')
        name = request.form.get('name')
        middle_name = request.form.get('middle_name')
        passport_data = request.form.get('passport_data')
        address = request.form.get('address')
        phone = request.form.get('phone')
        dateText = request.form.get('date')
        dt = datetime.now()
        dt.replace(year=int(dateText.split('-')[0]), month=int(dateText.split('-')[1]), day=int(dateText.split('-')[2]))
        insert_new_human(surname, name, middle_name, dt, passport_data, address, phone)
    return redirect('/menedger')


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
