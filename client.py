from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import time
import random
from dotenv import load_dotenv
import os

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
        time.sleep(random.uniform(0.3, 2.3))  # случайный перерыв проверки
        try:
            client.get_users(i)
            mi_list.append(i)
            tu_table_list.append(i)
        except Exception:
            tu_table_list.append('нет')
        if len(mi_list) == 4:
            break

    message.reply('\n'.join(mi_list))
    if len(mi_list) != len(tu_table_list):
        message.reply('\n'.join(tu_table_list))
    # message.reply(client.get_users('@al2151'))


client.run()
