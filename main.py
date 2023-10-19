import random
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
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
    if request.method == "POST":
        print(request.form)
        good_id = request.form['item_id']
        # TODO: Получить buyer_id
        db_add_good(good_id, 1)
    goods = get_products()
    print(goods)
    fields_name = ('good_id', 'name', 'description', 'price', 'image_path')
    dict_goods = list(map(lambda x: dict(zip(fields_name, x)), goods))
    return render_template('products.html', goods_to_html = dict_goods)
    # return render_template('products.html')

@app.route('/contacts/')
@login_required
def contacts():
    return render_template('contacts.html')


@app.route('/about/')
@login_required
def about():
    return render_template('about.html')


@app.route('/bag/', methods=['GET', 'POST'])
@login_required
def bag():
    goods_ids = get_goods_in_bag(1)
    print(goods_ids)
    goods = get_products_by_id(goods_ids)
    return render_template('bag.html', goods_to_html = goods)


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
        buyers = get_login(request.form['login'])
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
            if db_register(request.form) == 'UniqueViolation':
                return render_template("register.html", error_of_register="Пользователь с такими данными уже существует")
        return render_template("login.html")
    return render_template('register.html')


if __name__ == "__main__":
    app.run()