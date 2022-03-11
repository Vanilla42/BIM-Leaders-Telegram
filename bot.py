import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import datetime
import psycopg2

# Bot initiation
API_KEY = os.environ['TOKEN']
bot = telebot.TeleBot(API_KEY)


#----------------
# DATABASE
#----------------


# Database connection
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
cursor = connection.cursor()

# Wrapper
def db_handler(func):
    def wrap(*args, **kwargs):
        connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
        cursor = connection.cursor()
        data = func(*args, **kwargs)
        cursor.close()
        connection.close()
        return data
    return wrap

#@db_handler
def db_create_table():
    # date | user_id | item
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE shopping (col_date VARCHAR(64), col_user_id VARCHAR(64), col_item VARCHAR(64))")
    cursor.execute("INSERT INTO shopping (col_date, col_user_id, col_item) VALUES (%s, %s, %s)", ("Дата", "ID", "Товар"))
    connection.commit()
    cursor.close()
    connection.close()

    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    b = cursor.execute("SELECT * FROM shopping")
    cursor.close()
    connection.close()

    return b

def db_read_all():
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    data = cursor.execute('SELECT * FROM shopping ORDERBY col_user_id')
    if data == None:
        db_create_table()
    cursor.close()
    connection.close()
    return data

def db_read_user(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    data = cursor.execute('SELECT * FROM shopping WHERE col_user_id=%(user_id)s ORDERBY col_user_id')
    cursor.close()
    connection.close()
    return data

def db_add_row(date, user_id, item):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO shopping VALUES (%(date)s, %(user_id)s, %(item)s)')
    cursor.close()
    connection.close()
    return True


#----------------
# KITCHEN
#----------------

@bot.message_handler(commands=['kitchen'])
def kitchen_command(message):
  chat_id = message.chat.id
  bot.delete_message(message.chat.id, message.message_id)
  #message_bot_kitchen = bot.send_message(message.chat.id, kitchen_message(), reply_markup=markup_delete())
  message_bot_kitchen = bot.send_message(
    message.chat.id,
    kitchen_message(),
    parse_mode = "MarkdownV2",
    disable_notification=True
  )
  
  time.sleep(10)
  bot.delete_message(chat_id, message_bot_kitchen.message_id) 

def kitchen_message():
  time = get_time()
  timetxt = ""
  if time == 0:
    timetxt = "\U000023F0 *MORNING* \U000023F0"
  if time == 1:
    timetxt = "\U00002600 *DAY* \U00002600"
  if time == 2:
    timetxt = "\U0001F319 *EVENING* \U0001F319"
  workers = "\n".join(kitchen_workers[day][time])
  heplers = "\n".join(kitchen_heplers[day][time])
  message = timetxt + "\n\U0001F373 KITCHEN:\n" + workers + "\n" + "\U0001F37D HELP: \n" + heplers
  return message


day = datetime.datetime.today().weekday()

def get_time():
  hour = datetime.datetime.now().hour + 2
  t = 0         # Morning  0-10
  if hour > 10: # Day     10-15
    t = 1
  if hour > 15: # Evening 15-24
    t = 2
  return t

kitchen_workers = [
  [["Денис", "Альбіна"],["Крупка Назар", "Маша", "Артем"],["Слава", "Денис"]],
  [["Слава", "Артем"],["Авраменко Іван", "Олександр", "Альбіна"],["Крупка Назар", "Артем"]],
  [["Крупка Назар", "Денис"],["Маша", "Стас", "Слава"],["Альбіна", "Авраменко Іван"]],
  [["Авраменко Іван", "Олександр"],["Артем", "Денис", "Альбіна"],["Стас", "Крупка Назар"]],
  [["Маша", "Стас"],["Слава", "Альбіна", "Крупка Назар"],["Денис", "Артем"]],
  [["Савіна Юлія", "Тюріна Тіна"],["Денис", "Романюк Катерина", "Ганін Петро"],["Маша", "Цвігун Людмила"]],
  [["Зотіна Анастасія", "Авраменко Іван"],["Ткаченко Вікторія", "Слава", "Шавловська Яна"],["Наголюк Євген", "Авраменко Антоніна"]]
]
kitchen_heplers = [
  [["Півень Денис", "Авраменко Антоніна"],["Редчиць Денис", "Тюріна Тіна"],["Проскурня Михайло", "Зотіна Анастасія"]],
  [["Налогюк Євген", "Цвігун Людмила"],["Пінчук Іван", "Авраменко Іван"],["Романюк Катерина", "Чаур Анастасія"]],
  [["Ганін Петро", "Редчиць Денис"],["Ткаченко Вікторія", "Проскурня Михайло"],["Півень Денис", "Савіна Юлія"]],
  [["Шавловська Яна", "Романюк Катерина"],["Савіна Юлія", "Алєксєєв Еміль"],["Цвігун Людмила", "Редчиць Денис"]],
  [["Стас", "Чаур Анастасія"],["Півень Денис", "Зотіна Анастасія"],["Тюріна Тіна", "Алєксєєв Еміль"]],
  [["Крупка Назар", "Альбіна"],["Авраменко Іван", "Олександр"],["Авраменко Іван", "Ткаченко Вікторія"]],
  [["Пінчук Іван", "Алєксєєв Еміль"],["Авраменко Антоніна", "Чаур Анастасія"],["Проскурня Михайло", "Шавловська Яна"]]
]

#----------------
# SHOP
#----------------

@bot.message_handler(commands=['shop'])
def shop_command(message):
  bot.delete_message(message.chat.id, message.message_id)
  message_bot_shop = bot.send_message(
    message.chat.id,
    "Я допоможу із покупками\! Виберіть опцію нижче",
    reply_markup=shop_markup(),
    parse_mode = "MarkdownV2",
    disable_notification=True,
  )

@bot.message_handler
def shop_command_list(message):
  bot.send_chat_action(message.chat.id, 'typing') # The typing state into the chat, so the bot will display the “typing” indicator.
  bot.send_message(
    message.chat.id,
    db_read_all(),
    reply_markup=shop_markup_list(),
    parse_mode = "MarkdownV2",
    disable_notification=True
  )
  bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler
def shop_command_add(message):
  shop_message_add = bot.send_message(
    message.chat.id,
    db_read_all(),
    reply_markup=shop_markup_add(),
    parse_mode = "MarkdownV2",
    disable_notification=True,
  )
  return shop_message_add

@bot.message_handler
def shop_command_del(message):
  shop_message_del = bot.send_message(
    message.chat.id,
    db_read_all(),
    reply_markup=shop_markup_add(),
    parse_mode = "MarkdownV2",
    disable_notification=True
  )
  return shop_message_del

def shop_markup():
  markup = InlineKeyboardMarkup(row_width=3)
  btn1 = InlineKeyboardButton("\U0001F4C3 Список", callback_data="shop_call_list")
  btn2 = InlineKeyboardButton("\U00002795 Замовити", callback_data="shop_call_add")
  btn3 = InlineKeyboardButton("\U00002796 Відмінити", callback_data="shop_call_del")
  markup.add(btn1, btn2, btn3)
  return markup

def shop_markup_add():
  markup = InlineKeyboardMarkup(row_width=1)
  btn3 = InlineKeyboardButton("\U00002795 Назад", callback_data="shop_call")
  markup.add(btn1, btn2, btn3)
  return markup

def shop_markup_del():
  markup = InlineKeyboardMarkup(row_width=1)
  btn3 = InlineKeyboardButton("\U00002795 Назад", callback_data="shop_call")
  markup.add(btn1, btn2, btn3)
  return markup

def shop_markup_list():
  markup = InlineKeyboardMarkup(row_width=3)
  btn1 = InlineKeyboardButton("\U0001F4C3 Мой список", callback_data="shop_call_list_my")
  btn2 = InlineKeyboardButton("\U00002795 Весь список", callback_data="shop_call_list_all")
  btn3 = InlineKeyboardButton("\U00002795 Назад", callback_data="shop_call")
  markup.add(btn1, btn2, btn3)
  return markup

def shop_markup_list_all():
  markup = InlineKeyboardMarkup(row_width=3)
  btn1 = InlineKeyboardButton("\U0001F4C3 Замовити", callback_data="shop_call_add")
  btn2 = InlineKeyboardButton("\U00002795 Відмінити", callback_data="shop_call_del")
  btn3 = InlineKeyboardButton("\U00002795 Назад", callback_data="shop_call")
  markup.add(btn1, btn2, btn3)
  return markup

def shop_markup_list_my():
  markup = InlineKeyboardMarkup(row_width=3)
  btn1 = InlineKeyboardButton("\U0001F4C3 Замовити", callback_data="shop_call_add")
  btn2 = InlineKeyboardButton("\U00002795 Відмінити", callback_data="shop_call_del")
  btn3 = InlineKeyboardButton("\U00002795 Назад", callback_data="shop_call")
  markup.add(btn1, btn2, btn3)
  return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  if call.data == "shop_call_list":
    b = db_create_table()
    bot.send_message(call.message.chat.id, str(b), parse_mode = "MarkdownV2")
    shop_call_command_list(call)
  elif call.data == "shop_call_add":
    shop_call_command_add(call)
  elif call.data == "shop_call_del":
    shop_call_command_del(call)
  elif call.data == "shop_call_list_all":
    shop_call_command_list_all(call)
  elif call.data == "shop_call_list_my":
    shop_call_command_list_my(call)
  elif call.data == "shop_call":
    shop_call_command(call)
 
def shop_call_command_list(call):
   bot.answer_callback_query(call.id) # Required to remove the loading state, which appears upon clicking the button.
   shop_command_list(call.message)

def shop_call_command_add(call):
   bot.answer_callback_query(call.id) # Required to remove the loading state, which appears upon clicking the button.
   shop_command_add(call.message)

def shop_call_command_del(call):
   bot.answer_callback_query(call.id) # Required to remove the loading state, which appears upon clicking the button.
   shop_command_del(call.message)

"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  if call.data == "shop_markup_list":
    bot.answer_callback_query(call.id, "Answer is Yes")
  elif call.data == "shop_markup_add":
    bot.answer_callback_query(call.id, "Answer is No")
  elif call.data == "shop_markup_del":
    bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())
    #bot.reply_to(message, message_kitchen())
"""

bot.infinity_polling()