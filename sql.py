import psycopg2


def get_db_connection():
    conn = psycopg2.connect(host='db',
                            database='postgres',
                            user='postgres',
                            password='',
                            port=5432)
    return conn


script = """
    CREATE TABLE IF NOT EXISTS buyers (
        buyer_id serial PRIMARY KEY,
        login VARCHAR ( 50 ) UNIQUE NOT NULL,
        name VARCHAR ( 50 ) NOT NULL,
        password VARCHAR ( 50 ) NOT NULL,
        phone VARCHAR ( 20 ) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS goods (
        good_id serial PRIMARY KEY,
        name VARCHAR ( 255 ) NOT NULL,
        description TEXT NOT NULL,
        price numeric NOT NULL,
        image_path VARCHAR (255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS order_info (
        order_info_id serial PRIMARY KEY,
        name VARCHAR ( 50 ) NOT NULL,
        surname VARCHAR ( 50 ) NOT NULL,
        address VARCHAR ( 255 ) NOT NULL,
        phone VARCHAR ( 20 ) NOT NULL,
        date_of_order timestamp without time zone,
        deliver_date timestamp without time zone,
        deliver_type VARCHAR ( 50 ) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS orders (
        order_id serial PRIMARY KEY,
        buyer_id INT NOT NULL,
        good_id INT NOT NULL,
        amount INT NOT NULL,
        order_info_id int NOT NULL
    );
    ALTER TABLE orders
        ADD FOREIGN KEY (buyer_id) 
        REFERENCES buyers (buyer_id) 
        ON DELETE CASCADE;
    ALTER TABLE orders
        ADD FOREIGN KEY (good_id) 
        REFERENCES goods (good_id) 
        ON DELETE CASCADE;
    ALTER TABLE orders
        ADD FOREIGN KEY (order_info_id) 
        REFERENCES order_info (order_info_id) 
        ON DELETE CASCADE;
    CREATE TABLE IF NOT EXISTS bags (
        bag_id serial PRIMARY KEY,
        buyer_id INT NOT NULL,
        good_id INT NOT NULL,
        amount INT NOT NULL
    );
    ALTER TABLE bags
        ADD FOREIGN KEY (buyer_id) 
        REFERENCES buyers (buyer_id) 
        ON DELETE CASCADE;
    ALTER TABLE bags
        ADD FOREIGN KEY (good_id) 
        REFERENCES goods (good_id) 
        ON DELETE CASCADE;
"""
data = [{'name': 'Супер крутой товар', 'description': 'Это супер крутой товар, скорее покупай', "price": 50,
         'image_path': "куб.jpeg"},
        {'name': 'Супер крутой товар2', 'description': 'Это супер крутой товар, скорее покупай2', "price": 500,
         'image_path': "top_good.jpg"},
        {'name': "fsf", 'description': 'sdfsdefs', 'price': 545, "image_path": "54564"}]
con = get_db_connection()
cursor = con.cursor()
cursor.execute(script)
con.commit()
for good in data:
    cursor.execute('INSERT INTO goods(name, description, price, image_path) \
                    VALUES(%s,%s,%s,%s);'
                   , (good['name'], good['description'], good['price'], good['image_path']))
con.commit()
cursor.close()
con.close()
