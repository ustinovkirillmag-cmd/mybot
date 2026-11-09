import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить тутор на качество", callback_data="buy")],
    [
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Поддержка", callback_data="support"),
    ],
])

@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    name = f"@{user.username}" if user.username else user.first_name
    await message.answer(f"Привет, {name}!", reply_markup=keyboard)

@dp.callback_query(F.data == "buy")
async def buy(call: CallbackQuery):
    await call.message.answer("Скоро здесь появится покупка.")
    await call.answer()

@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    await call.message.answer(f"Твой ID: {call.from_user.id}")
    await call.answer()

@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await call.message.answer("Напиши в поддержку.")
    await call.answer()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
