import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import datetime
import psycopg2


# Database connection
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
cursor = connection.cursor()

def create_db_table():
    # date | user_id | item
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE shopping (col_date VARCHAR(64), col_user_id VARCHAR(64), col_item VARCHAR(64))")
    cursor.close()
    connection.close()
    return True

def read_db_all():
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    data = cursor.execute('SELECT * FROM shopping ORDERBY col_user_id')
    cursor.close()
    connection.close()
    return data

def read_db_user(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    data = cursor.execute('SELECT * FROM shopping WHERE col_user_id=%(user_id)s ORDERBY col_user_id')
    cursor.close()
    connection.close()
    return data

def add_db_row(date, user_id, item):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO shopping VALUES (%(date)s, %(user_id)s, %(item)s)')
    cursor.close()
    connection.close()
    return True


# Bot initiation
API_KEY = os.environ['TOKEN']
bot = telebot.TeleBot(API_KEY)


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

def message_kitchen():
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

@bot.message_handler(commands=['kitchen'])
def kitchen(message):
  chat_id = message.chat.id
  bot.delete_message(chat_id, message.message_id)
  #message_bot_kitchen = bot.send_message(message.chat.id, message_kitchen(), reply_markup=markup_delete())
  message_bot_kitchen = bot.send_message(chat_id, message_kitchen(), parse_mode 
 = "MarkdownV2", disable_notification=True)
  
  time.sleep(10)
  bot.delete_message(chat_id, message_bot_kitchen.message_id) 
  
@bot.message_handler(commands=['shop'])
def shop(message):
  chat_id = message.chat.id
  bot.delete_message(chat_id, message.message_id)
  #message_bot_kitchen = bot.send_message(message.chat.id, message_kitchen(), reply_markup=markup_delete())
  message_bot_kitchen = bot.send_message(chat_id, message_kitchen(), parse_mode 
 = "MarkdownV2", disable_notification=True)
  
  time.sleep(10)
  bot.delete_message(chat_id, message_bot_kitchen.message_id) 

"""
def gen_markup():
  markup = InlineKeyboardMarkup()
  markup.row_width = 2
  markup.add(InlineKeyboardButton("Kitchen", callback_data="cb_yes"), InlineKeyboardButton("No", callback_data="cb_no"))
  return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  if call.data == "cb_yes":
    bot.answer_callback_query(call.id, "Answer is Yes")
  elif call.data == "cb_no":
    bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())
    #bot.reply_to(message, message_kitchen())
"""

bot.infinity_polling()
