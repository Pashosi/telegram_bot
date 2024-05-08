from pyrogram import Client, errors
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time
import random
from dotenv import load_dotenv
import os
import sqlite3 as sq
from datetime import datetime


# создание базы данных
with sq.connect('tg_ex.db') as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        date datetime,
        count_id int
        )""")

def update_base(date: int):    #заносит дату и количество в базу
    with sq.connect('tg_ex.db') as con:
        cur = con.cursor()

        data = datetime.now()
        count = date

        sql = "INSERT INTO users VALUES (?, ?)"
        cur.execute(sql, (data, count))


# Вставляем api_id и api_hash
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = Client(name='me_client', api_id=api_id, api_hash=api_hash)


@client.on_message()  # декоратор хендлеров
def all_message(client: Client, message: Message):
    text = message.text.split('\n')
    mi_list = []
    tu_table_list = []

    for i in text:
        time.sleep(random.uniform(0.4, 2.3))  # случайный перерыв проверки
        try:
            # print(len(mi_list)+1, f'"{client.get_users(i).__getattribute__("username")}"',
            #       client.get_users(i).__getattribute__('id'))
            print(len(mi_list) + 1, client.get_users(i).username, client.get_users(i).id)
            # print(dir(client.get_users(i)))
        except errors.exceptions.bad_request_400.UsernameNotOccupied as ex:
            print(ex.MESSAGE, ex.CODE)
        except errors.exceptions.bad_request_400.UsernameInvalid as ex:
            print(ex.MESSAGE, ex.CODE)
        except Exception as ex:
            print(ex, ex.args)

        try:
            client.get_users(i)
            mi_list.append(i)
            tu_table_list.append(i)
        except Exception:
            tu_table_list.append('нет')
        if len(mi_list) == 21:
            break

    if len(mi_list) > 0:
        message.reply('\n'.join(mi_list))
        if len(mi_list) != len(tu_table_list):
            message.reply('\n'.join(tu_table_list))
        message.reply(f'первый список{len(mi_list)}, второй{len(tu_table_list)}')
        update_base(len(tu_table_list))
    else:
        print('список после проверки пуст')
        message.reply('список после проверки пуст')
    # message.reply(client.get_users('@al2151'))


client.run()
