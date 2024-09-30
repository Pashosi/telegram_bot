from pyrogram import Client, errors
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time
import random
from dotenv import load_dotenv
import os
import sqlite3 as sq
from datetime import datetime, timedelta

# создание базы данных
with sq.connect('tg_ex.db') as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        date datetime,
        count_id int
        )""")


def update_base(date: int):  # заносит дату и количество в базу
    with sq.connect('tg_ex.db') as con:
        cur = con.cursor()

        data = datetime.now()
        count = date

        sql = "INSERT INTO users VALUES (?, ?)"
        cur.execute(sql, (data, count))


def time_wait(sec):
    """Ожидание разблокироки из-за частых запросов. С переодичностью выводом на экран времени ожидания"""
    print(f'Ожидание={sec}сек')
    wait_datatime = datetime.now() + timedelta(seconds=sec)
    for num in range(sec, 0, -5):
        print(f'Осталось {num} сек, проверено {datetime.now()}, будет все готово в {wait_datatime}')
        time.sleep(5)
    # time.sleep(sec)


# Вставляем api_id и api_hash
load_dotenv()
api_id = os.getenv('API_ID_L')
api_hash = os.getenv('API_HASH_L')

client = Client(name='me_client', api_id=api_id, api_hash=api_hash)


# print(client.__dict__)

def get_greeting(num: int):
    if isinstance(num, int) and 0 < num < 6:
        greet_dict = {
            1: ('Здравствуйте😊', 'Приветствую😊'),
            2: ('Здравствуйте👋', 'Приветствую👋'),
            3: ('Здравствуйте✌️', 'Приветствую✌️'),
            4: ('Здравствуйте!', 'Добрый день😊'),
            5: ('Добрый день👋', 'Добрый день✌️'),
        }
        return greet_dict[num]
    return 'Нет такого приветствия'


def update_dog_text(nik: str):
    """Добавление собаки в ник и удаление пробелов если не начин с @"""
    if not nik.startswith('@'):
        return f'@{"".join(nik.split())}'
    return nik


@client.on_message()  # декоратор хендлеров
def all_message(client: Client, message: Message):
    text = message.text.split('\n')
    mi_list = []
    tu_table_list = []
    check_greet = True

    if text[0] in ['1', '2', '3', '4', '5']:
        message.reply(get_greeting(int(text[0]))[0])
        message.reply(get_greeting(int(text[0]))[1])

    else:
        for i in text:
            time.sleep(random.uniform(0.9, 2.3))  # случайный перерыв проверки
            try:
                print(len(mi_list) + 1, client.get_users(i).username, client.get_users(i).id)
            except errors.exceptions.bad_request_400.UsernameNotOccupied as ex:
                print(ex.MESSAGE, ex.CODE)
            except errors.exceptions.bad_request_400.UsernameInvalid as ex:
                print(ex.MESSAGE, ex.CODE)
            except errors.exceptions.flood_420.FloodWait as ex:
                print('Отлов ошибки за флуд', ex.ID, ex.MESSAGE, ex.value)
                if hasattr(ex, 'value'):
                    time_wait(ex.value)
            except Exception as ex:
                print(ex.__dict__)
                if hasattr(ex, 'value'):
                    time_wait(ex.value)

            try:
                client.get_users(update_dog_text(i))
                mi_list.append(update_dog_text(i))
                tu_table_list.append(update_dog_text(i))
            except Exception:
                tu_table_list.append('нет')
            if len(mi_list) == 23:
                break

        if len(mi_list) > 0 and check_greet == True:
            message.reply('\n'.join(mi_list))
            if len(mi_list) != len(tu_table_list):
                message.reply('\n'.join(tu_table_list))
            message.reply(f'первый список{len(mi_list)}, второй{len(tu_table_list)}')
            update_base(len(tu_table_list))
        else:
            print('список после проверки пуст')
            message.reply('список после проверки пуст')


client.run()
