import random
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from psycopg2.errors import UniqueViolation
from db_functions import *


app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'Top secret'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(login):
        return User(login)
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/products/', methods=['GET', 'POST'])
@login_required
def products():
    goods = get_products()
    print(goods)
    return render_template('products.html', goods_to_html = goods)
    # return render_template('products.html')

@app.route('/contacts/')
@login_required
def contacts():
    return render_template('contacts.html')


@app.route('/about/')
@login_required
def about():
    return render_template('about.html')


@app.route('/bag/')
@login_required
def bag():
    return render_template('bag.html')


@app.route('/product1/')
@login_required
def product1():
    end_date = '2024.09.01'
    date = datetime.strptime(end_date, '%Y.%m.%d')
    diff = date - datetime.now()
    days_before_end = diff.days
    num = random.randint(1,5)
    return render_template('product1.html', action_name='Весенние скидки!', end_date=end_date, days_before_end = days_before_end, num = num)


@app.route('/product2/')
@login_required
def product2():
    end_date = '2024.09.01'
    date = datetime.strptime(end_date, '%Y.%m.%d')
    diff = date - datetime.now()
    days_before_end = diff.days
    return render_template('product1.html', action_name='Весенние скидки!', end_date=end_date, days_before_end=days_before_end)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        connection = get_db_connection()
        cursor = connection.cursor()
        # Выполнение SQL-запроса для вставки данных в таблицу
        cursor.execute('select login, password from buyers \
                            where login = (%s);'
                    , (request.form["login"],))
        buyers = cursor.fetchall()
        cursor.close()
        connection.close()
        print(buyers)
        if len(buyers) == 0:
            return render_template('login.html', error_of_loginning = "Неверный логин")
        if request.form['password'] != buyers[0][1]:
            return render_template('login.html', error_of_loginning="Неверный пароль")
        user = User(login)  # Создаем пользователя
        login_user(user)  # Логиним пользователя
        return render_template('index.html')
    return render_template('login.html')

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return "Пока"

@app.route('/register/', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form["password"] != request.form["password2"]:
            return render_template('register.html', error_of_register="Пароли не совпадают")
        for item in request.form:
            if request.form[item] == "":
                return render_template('register.html', error_of_register="Все поля должны быть заполнены!")
        conn = get_db_connection()  # открываем connection
        cur = conn.cursor()  # ставим курсор
        # выполняем операцию по вставке
        try:
            cur.execute('INSERT INTO buyers(login, name, password, phone) \
                    VALUES(%s,%s,%s,%s);'
                    , (request.form["login"], request.form["name"], request.form["password"], request.form["phone"]))
        except UniqueViolation as e:
            cur.close()
            conn.close()
            return render_template("register.html", error_of_register= "Пользователь с такими данными уже существует")
        conn.commit()  # сохраняем изменения в базе
        cur.close()  # убираем курсор и закрываем connection
        conn.close()
        return render_template("login.html")
    return render_template('register.html')


if __name__ == "__main__":
    app.run()