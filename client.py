from pyrogram import Client, errors
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
        time.sleep(random.uniform(0.4, 2.3))  # случайный перерыв проверки
        try:
            # print(len(mi_list)+1, f'"{client.get_users(i).__getattribute__("username")}"',
            #       client.get_users(i).__getattribute__('id'))
            print(len(mi_list) + 1, client.get_users(i).username, client.get_users(i).id)
            # print(dir(client.get_users(i)))
        except errors.exceptions.bad_request_400.UsernameNotOccupied as ex:
            print(ex.MESSAGE)
        except errors.exceptions.bad_request_400.UsernameInvalid as ex:
            print(ex.MESSAGE)
        # except IndexError as ex:
        #     print(ex)
        # except KeyError as ex:
        #     print(ex)
        # except TypeError as ex:
        #     print(ex)
        # except errors.exceptions as ex:
        #     print(ex)
        except Exception as ex:
            print(ex)

        try:
            client.get_users(i)
            mi_list.append(i)
            tu_table_list.append(i)
        except Exception:
            tu_table_list.append('нет')
        if len(mi_list) == 22:
            break

    if len(mi_list) > 0:
        message.reply('\n'.join(mi_list))
        if len(mi_list) != len(tu_table_list):
            message.reply('\n'.join(tu_table_list))
        message.reply(f'первый список{len(mi_list)}, второй{len(tu_table_list)}')
    else:
        print('список после проверки пуст')
        message.reply('список после проверки пуст')
    # message.reply(client.get_users('@al2151'))


client.run()
