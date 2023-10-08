import telebot
from newsapi import NewsApiClient
from telebot import types
import sqlite3

bot = telebot.TeleBot("6359000148:AAEyE6easMVL7pMp3H2K_NnL_N9BmczAtDA", parse_mode=None)
news_key = 'fa26ad0dfe444a55955c5b6208e61e2e'
newsapi = NewsApiClient(api_key=news_key)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  userID = message.from_user.id
  connect = sqlite3.connect('bd.db')
  cursor = connect.cursor()
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

  btn_news = types.KeyboardButton('новости')
  btn_subscribes = types.KeyboardButton('подписки')
  btn_category = types.KeyboardButton('категории')
  markup.add(btn_news, btn_subscribes, btn_category)

  user = cursor.execute('SELECT * FROM users WHERE tg_id = ?;', (userID,)).fetchall()
  if not user:
    cursor.execute('''INSERT INTO users ('tg_id') VALUES (?);''', (userID,))
    connect.commit()
    bot.reply_to(message, "вы зарегистрированы ", reply_markup=markup)
  else:
    bot.reply_to(message, "вы уже зарегистрированы", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
  print(message.text)
  if message.chat.type == 'private':
    if message.text == 'категории':
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      connect = sqlite3.connect('bd.db')
      cursor = connect.cursor()
      categories = cursor.execute('SELECT id, name FROM categories;').fetchall()
      print(categories)
      i = 0
      while i < len(categories):
          name = str(categories[i][0])
          name = types.KeyboardButton('+ ' +categories[i][1])
          markup.add(name)
          i = i + 1
      back = types.KeyboardButton('назад')
      markup.add(back)
      bot.reply_to(message, "вы можете подписаться на:", reply_markup=markup)


  if message.chat.type == 'private':
    check = '+ '
    if message.text.startswith(check):
        userID = message.from_user.id
        connect = sqlite3.connect('bd.db')
        cursor = connect.cursor()
        id = cursor.execute('SELECT id FROM users WHERE tg_id=?;', (userID,)).fetchone()
        id = str(id[0])
        sub = cursor.execute('SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.category_id WHERE user_id = ?;',(id,)).fetchall()
        arr_subscribes = []
        i = 0
        while i < len(sub):
            arr_subscribes.append(sub[i][3])
            i = i + 1
        i = 0
        count = 0
        name_subscribes = message.text[2:]
        while i < len(arr_subscribes):
            if name_subscribes == arr_subscribes[i]:
                count = count + 1
            i = i + 1
        if count == 0:
            category_id = cursor.execute('SELECT id FROM categories WHERE name = ?;', (name_subscribes,)).fetchall()
            cursor.execute('''INSERT INTO subscribes('user_id', 'category_id') VALUES(?,?);''', (id, category_id[0][0]))
            connect.commit()
            bot.reply_to(message, "вы подписались!")
        else:
            bot.reply_to(message, "вы уже подписаны)")


    if message.chat.type == 'private':
          if message.text == 'подписки':
              markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
              userID = message.from_user.id
              connect = sqlite3.connect('bd.db')
              cursor = connect.cursor()
              id = cursor.execute('SELECT id FROM users WHERE tg_id = ?;', (userID,)).fetchone()
              id = str(id[0])
              sub = cursor.execute('SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.category_id WHERE user_id = ?;',(id,)).fetchall()
              arr_subscribes = []
              i = 0
              while i < len(sub):
                  arr_subscribes.append(sub[i][3])
                  i = i + 1
              i = 0
              while i < len(arr_subscribes):
                  name = str(arr_subscribes[i])
                  name = types.KeyboardButton('- ' +arr_subscribes[i])
                  markup.add(name)
                  i = i + 1
              back = types.KeyboardButton('назад')
              markup.add(back)
              bot.reply_to(message, "вы подписаны на: \nнажмите,чтобы отписаться :3", reply_markup=markup)


    if message.chat.type == 'private':
        check = "- "
        if message.text.startswith(check):
            userID = message.from_user.id
            connect = sqlite3.connect('bd.db')
            cursor = connect.cursor()
            id = cursor.execute('SELECT id FROM users WHERE tg_id = ?;', (userID,)).fetchone()
            id = str(id[0])
            name_category = message.text[2:]
            category_id = cursor.execute('SELECT id FROM categories WHERE name = ?;', (name_category,)).fetchall()
            category_id = category_id[0][0]
            check_subscribes = cursor.execute('SELECT * FROM subscribes WHERE user_id = ? and category_id = ?;', (id, category_id)).fetchone()

            if not check_subscribes:
                bot.reply_to(message, "вы не подписаны")
            else:
                cursor.execute('DELETE FROM subscribes WHERE user_id = ? and category_id = ?;', (id, category_id))
                connect.commit()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                sub = cursor.execute(
                    'SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.category_id WHERE user_id = ?;', (id,)).fetchall()
                arr_subscribes = []
                i = 0
                while i < len(sub):
                    arr_subscribes.append(sub[i][3])
                    i = i + 1
                i = 0
                while i < len(arr_subscribes):
                    name = str(arr_subscribes[i])
                    name = types.KeyboardButton('- ' +arr_subscribes[i])
                    markup.add(name)
                    i = i + 1
                back = types.KeyboardButton('назад')
                markup.add(back)
                bot.reply_to(message, "вы отписались :с\nнажмите,чтобы отписаться :3", reply_markup=markup)


    if message.chat.type == 'private':
          if message.text == 'новости':

              userID = message.from_user.id
              connect = sqlite3.connect('bd.db')
              cursor = connect.cursor()
              id = cursor.execute('SELECT id FROM users WHERE tg_id=?;', (userID,)).fetchone()
              id = str(id[0])
              sub = cursor.execute('SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.category_id WHERE user_id = ?;',(id,)).fetchall()
              i = 0
              while i < len(sub):
                  top_headlines = newsapi.get_top_headlines(category=f'{sub[i][4]}', language='ru', country='ru', page=1,page_size=1)
                  bot.send_message(message.chat.id,f'категория: {sub[i][3]}\nзаголовок: {top_headlines["articles"][0]["title"]}\n{top_headlines["articles"][0]["url"]}')
                  i = i + 1


  if message.chat.type == 'private':
    if message.text == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_news = types.KeyboardButton('новости')
        btn_subscribes = types.KeyboardButton('подписки')
        btn_category = types.KeyboardButton('категории')
        markup.add(btn_category, btn_news, btn_subscribes)
        bot.reply_to(message, ":D", reply_markup=markup)


bot.infinity_polling(none_stop=True)



