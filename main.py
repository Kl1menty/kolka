import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import random as rd
import re

# === ЗАГРУЖАЕМ ПЕРЕМЕННЫЕ ИЗ .env ===
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
active_groups = {}  # словарь для статуса бота в каждой группе
Spisok_nahuy = ['Так блять', 'Сука нахуй', 'Так нахуй', 'Нихуево', 'Нихуево блять', 'Посос', 'Наебка', 'Ну а хули']
BAD_WORDS = [
    r'б+л+я+',  # бля, бляяять
    r'с+у+к+',  # сука, суууука
    r'х+у+[йеяю]+',  # хуй, хуя, хуево
    r'н+а+е+б+',  # наеб, наебка
    r'н+и+х+у+[еёя]+',
    r'п+о+х+у+[йеяю]+',
]

if not API_TOKEN:
    raise ValueError("Не найден токен! Добавь его в .env как BOT_TOKEN=...")

# === СОЗДАНИЕ БОТА И ДИСПЕТЧЕРА ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# === ОБРАБОТЧИКИ ===
# @dp.message(Command("start"))
# async def start_handler(message: types.Message):
#     await message.answer("Привет! Я бот 🤖")
#
#
# @dp.message(Command("help"))
# async def help_handler(message: types.Message):
#     await message.answer("Список команд:\n/start — запуск\n/help — помощь")

@dp.message(Command("start"))
async def start_bot(m: types.Message):
    chat_id = m.chat.id
    active_groups[chat_id] = True
    await m.reply(".✅")


@dp.message(Command("stop"))
async def stop_bot(m: types.Message):
    chat_id = m.chat.id
    active_groups[chat_id] = False
    await m.reply(".❌")


@dp.message(lambda m: m.text and any(re.search(word, m.text.lower()) for word in BAD_WORDS))
async def reply_swear(msg: types.Message):
    # проверяем, включен ли бот для этой группы
    if not active_groups.get(msg.chat.id, True):
        return  # бот отключен — ничего не делаем
    await msg.reply(rd.choice(Spisok_nahuy))


# === ЗАПУСК ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
