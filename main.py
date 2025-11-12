import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import random as rd
import re

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
active_groups = {}  # словарь для статуса бота в каждой группе
Spisok_nahuy = ['Так блять', 'Сука нахуй', 'Так нахуй', 'Нихуево', 'Нихуево блять', 'Посос', 'Наебка', 'Ну а хули',
                'Так то похуй']
BAD_WORDS = [
    r'б+л+я+',
    r'с+у+к+',
    r'х+у+[йеяю]+',
    r'н+а+е+б+',
    r'н+и+х+у+[еёя]+',
    r'п+о+х+у+[йеяю]+',
    r'п+о+с+о+с+',
]

if not API_TOKEN:
    raise ValueError("Не найден токен! Добавь его в .env как BOT_TOKEN=...")

# === СОЗДАНИЕ БОТА И ДИСПЕТЧЕРА ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_bot(msg: types.Message):
    chat_id = msg.chat.id
    active_groups[chat_id] = True
    await msg.reply("Ну погнали хули✅")


@dp.message(Command("stop"))
async def stop_bot(msg: types.Message):
    chat_id = msg.chat.id
    active_groups[chat_id] = False
    await msg.reply("Стоп нахуй❌")


@dp.message(lambda m: m.text and 'брат' in m.text)
async def reply_swear(msg: types.Message):
    await msg.reply("макана больше слушай")


@dp.message(lambda m: m.text and '2' in m.text)
async def reply_swear(msg: types.Message):
    await msg.reply("Посос")


@dp.message(lambda m: m.text and m.text[-1] == '?')
async def reply_swear(msg: types.Message):
    await msg.reply("Айда!")


@dp.message(lambda m: m.text and any(re.search(word, m.text.lower()) for word in BAD_WORDS))
async def reply_swear(msg: types.Message):
    if not active_groups.get(msg.chat.id, True):
        return
    await msg.reply(rd.choice(Spisok_nahuy))


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

