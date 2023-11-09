import psycopg2
import datetime
from psycopg2.errors import UniqueViolation


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='test',
                            user='postgres',
                            password='An230909*#')
    return conn


# определение функции декоратора
def db_conn(input_func):
    def output_func(*args):  # определяем функцию, которая будет выполняться вместо оригинальной
        conn = get_db_connection()
        cur = conn.cursor()
        # print("*****************")  # перед выводом оригинальной функции выводим всякие звездочки
        res = input_func(cur, conn, *args)  # вызов оригинальной функции
        cur.close()
        conn.close()
        # print("*****************")  # после вывода оригинальной функции выводим всякие звездочки
        return res

    return output_func  # возвращаем новую функцию


@db_conn
def get_products(cur, conn):
    cur.execute('select * from goods')
    goods = cur.fetchall()
    return goods


@db_conn
def get_products_by_id(cursor, conn, ids):
    goods = []
    for id, amount in ids:
        cursor.execute('SELECT name, price, image_path, good_id from goods where good_id = (%s);', (id,))
        good = cursor.fetchall()[0]
        good_dict = {'name': good[0], "price": good[1], 'image_path': good[2],
                     'amount': amount, 'total': amount * good[1], 'good_id': good[3]}
        goods.append(good_dict)
    return goods


@db_conn
def get_login(cursor, conn, login):
    cursor.execute('select buyer_id, login, password from buyers \
                                where login = (%s);'
                   , (login,))
    buyers = cursor.fetchall()
    return buyers


@db_conn
def db_register(cur, conn, request_form):
    # выполняем операцию по вставке
    try:
        cur.execute('INSERT INTO buyers(login, name, password, phone) \
                        VALUES(%s,%s,%s,%s);'
                    , (request_form["login"], request_form["name"], request_form["password"], request_form["phone"]))
    except UniqueViolation as e:
        return 'UniqueViolation'
    conn.commit()  # сохраняем изменения в базе


@db_conn
def get_goods_in_bag(cursor, conn, buyer_id):
    cursor.execute('select good_id, amount from bags \
                                                    where buyer_id = (%s);'
                   , (buyer_id,))
    db_bag = cursor.fetchall()
    return db_bag


@db_conn
def db_add_good(cursor, conn, good_id, buyer_id):
    cursor.execute('select bag_id, amount from bags \
                                                        where good_id = (%s) and buyer_id  = (%s);'
                   , (good_id, buyer_id))
    bag = cursor.fetchall()
    if bag:
        cursor.execute('UPDATE bags set amount = (%s) where bag_id = (%s);'
                       , (bag[0][1] + 1, bag[0][0]))
    else:
        cursor.execute('INSERT INTO bags(good_id, buyer_id, amount) \
                                    VALUES(%s,%s,%s);'
                       , (good_id, buyer_id, 1))
    conn.commit()


@db_conn
def db_del_good(cursor, conn, good_id, buyer_id):
    cursor.execute('delete from bags \
                                    where good_id = (%s) and buyer_id  = (%s);'
                   , (good_id, buyer_id))
    conn.commit()


@db_conn
def db_move_bag_to_order(cursor, conn, buyer_id, request_form):
    cursor.execute("INSERT INTO order_info(name, surname, adress, phone, date_of_order, date, delivery_type) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s) returning order_info_id", (request_form["name"],
                                                                                           request_form["surname"],
                                                                                           request_form["adress"],
                                                                                           request_form["phone"],
                                                                                           datetime.datetime.now(),
                                                                                           request_form["date"],
                                                                                           request_form[
                                                                                            "delivery_type"]))
    order_info_id = cursor.fetchall()[0][0]
    cursor.execute('delete from bags \
                                        where buyer_id  = (%s) returning buyer_id, good_id, amount;'
                  , (buyer_id,))
    bag = cursor.fetchall()
    for good in bag:
        cursor.execute("INSERT INTO orders(buyer_id, good_id, amount, order_info_id) \
                          VALUES(%s, %s, %s, %s);", (good[0], good[1], good[2], order_info_id))
    conn.commit()
