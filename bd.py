from main import *
connect = sqlite3.connect('database/bd.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS "users" ("id" Integer not null, "tg_id" Integer not null, primary key("id" AUTOINCREMENT));''')
connect.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS "categories" ("id" Integer not null, "name" Text not null, "value" Text not null, primary key("id" AUTOINCREMENT));''')
connect.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS "subscribes" ("user_id" Integer not null, "category_id" Integer not null);''')
connect.commit()

# cursor.execute('''INSERT INTO categories (name,value) VALUES ("бизнес", "business")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("спорт", "sports")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("технологии", "techology")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("главное", "general")''')
# cursor.execute('''INSERT INTO categories (name,value) VALUES ("развлечение", "entertainment")''')
# connect.commit()