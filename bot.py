import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Купить тутор на качество")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    name = f"@{user.username}" if user.username else user.first_name
    await message.answer(f"Привет, {name}!", reply_markup=keyboard)

@dp.message(F.text == "Купить тутор на качество")
async def buy(message: Message):
    await message.answer("Скоро здесь появится покупка.")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
