import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                                database='test',
                                user='postgres',
                                password='An230909*#')
    return conn
data = [{'name': 'Супер крутой товар', 'description': 'Это супер крутой товар, скорее покупай', "price": 50, 'image_path': "куб.jpeg"},
        {'name': 'Супер крутой товар2', 'description': 'Это супер крутой товар, скорее покупай2', "price": 500, 'image_path': "top_good.jpg"},
        {'name': "fsf", 'description': 'sdfsdefs', 'price': 545, "image_path": "54564"}]
con = get_db_connection()
cursor = con.cursor()
for good in data:
    cursor.execute('INSERT INTO goods(name, description, price, image_path) \
                    VALUES(%s,%s,%s,%s);'
                    ,(good['name'], good['description'], good['price'], good['image_path']))
con.commit()
cursor.close()
con.close()