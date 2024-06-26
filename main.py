import telebot
import webbrowser
import os
import sqlite3
from telebot import types
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


name = None
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('base_date.sql') #подключение к файлу
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), password VARCHAR(50))')
    conn.commit() #синхронизация
    cur.close() #закрытие курсорв
    conn.close() #закрытие файла

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введи данные')
    bot.register_next_step_handler(message, user_name)
    # markup = types.ReplyKeyboardMarkup()
    # btn1 = types.KeyboardButton('перейти на сайт')
    # markup.row(btn1)
    # btn2 = types.KeyboardButton('удалить фото')
    # btn3 = types.KeyboardButton('изменить текст')
    # markup.row(btn2, btn3)
    # file = open('./photo.jpeg', 'rb')
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    # # bot.send_audio(message.chat.id, file, reply_markup=markup)
    # # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
     password = message.text.strip()
     conn = sqlite3.connect('base_date.sql')
     cur = conn.cursor()

     cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))
     conn.commit()
     cur.close()
     conn.close()

     markup = telebot.types.InlineKeyboardMarkup()
     markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
     bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
     # bot.send_message(message.chat.id, 'Введите пароль')
     # bot.register_next_step_handler(message, user_name)


def on_click(message):
    if message.text == 'перейти на сайт':
        bot.send_message(message.chat.id, 'сайт открыт')
    elif message.text == 'удалить фото':
        bot.send_message(message.chat.id, 'фото удалено')
    # bot.register_next_step_handler(message, on_click)
    # elif message.text == 'site':




@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('перейти на сайт', url='https://translate.google.ru/?hl=ru&tab=TT')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'какое красивое фото', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    # webbrowser.open('https://stepik.org/users/565204187/profile')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('сайт', url='https://translate.google.ru/?hl=ru&tab=TT')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'сайт', reply_markup=markup)


@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<u>Помощь</u>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)
