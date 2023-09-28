import psycopg2


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
        res = input_func(cur, *args)  # вызов оригинальной функции
        cur.close()
        cur.close()
        # print("*****************")  # после вывода оригинальной функции выводим всякие звездочки
        return res
    return output_func  # возвращаем новую функцию

@db_conn
def get_products(cur):
    cur.execute('select * from goods')
    goods = cur.fetchall()
    return goods