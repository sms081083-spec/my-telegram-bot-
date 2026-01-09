import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ←←← ОБЯЗАТЕЛЬНО ЗАМЕНИ НА СВОЙ ТОКЕН ОТ @BotFather ←←←
TOKEN = "7877970193:AAEBe5si7UR_dnZAmE9DTiiL_ytALRFeGts"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! 👋 Я твой бот, запущенный на Render!\nЯ работаю круглосуточно. Напиши что угодно — я повторю.")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
