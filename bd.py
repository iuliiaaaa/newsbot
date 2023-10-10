# from main import *
import sqlite3
connect = sqlite3.connect('bd.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS "users" ("id" Integer not null, "tg_id" Integer not null, primary key("id" AUTOINCREMENT));''')
connect.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS "categories" ("id" Integer not null, "name" Text not null, "value" Text not null, primary key("id" AUTOINCREMENT));''')
connect.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS "subscribes" ("user_id" Integer not null, "category_id" Integer not null);''')
connect.commit()

arr = [['бизнес', 'business'], ['спорт', 'sports'], ['технологии', 'technology'], ['главное', 'general'], ['развлечение', 'entertainment']]
category = cursor.execute('''SELECT * from categories''').fetchone()

if category == None:
    for i in arr:
        cursor.execute('''INSERT INTO categories (name, value) VALUES (?, ?);''',(i[0], i[1]))
        connect.commit()


# cursor.execute('''INSERT INTO categories (name,value) VALUES ("бизнес", "business")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("спорт", "sports")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("технологии", "technology")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("главное", "general")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("развлечение", "entertainment")''')
# connect.commit()
# arr_ru = ['бизнес', 'спорт', 'технологии', 'главное', 'развлечение']
# arr_eng = ['business', 'sports', 'technology', "general", 'entertainment']

