import logging
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from config import token
logging.basicConfig(level=logging.INFO)

conn =sqlite3.connect('python_group.db')
conn.execute('''create table if not exists message(
                first_name text,
                last_name text,
                data text
            );''')
conn.commit()
conn.close()

bot = Bot(token=token)
dp = Dispatcher(bot)

# __________________________KLIENT_CHAT_______________________________
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print(message.from_user.full_name)
    now = datetime.now()
    await message.reply("Assalomu aleykum tozolovchi botga hush kelibsiz!")

    getData = (message.from_user.first_name, message.from_user.last_name,f"{now.hour}:{now.minute}:{now.second}" )
    conn = sqlite3.connect('python_group.db')
    conn.execute('insert into message values(?,?,?)', getData)
    conn.commit()
    conn.close()

@dp.message_handler(commands='members')
async def send_welcome(message: types.Message):
    conn = sqlite3.connect('python_group.db')
    data =conn.execute('select * from message;')
    await message.reply(f'{data.fetchall()}')

@dp.message_handler()
async def send_welcome(message: types.Message):
    print(message.text)
    await message.reply('qoyil!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)