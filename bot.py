import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

ADMIN_ID = 8370155327
PAY_INFO = "79407315708 (СБП), получатель: Кирилл У."
PRICE = 150
TUTOR_TEXT = "Спасибо за покупку! Твой тутор - https://disk.yandex.ru/d/bbnygT5kKhcGxA"
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMG_20261109_134317_956.jpg")

HD_TEXT = (вот тутор как выкладывать с hd качеством https://disk.yandex.ru/d/bbnygT5kKhcGxA)
main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить тутор на качество", callback_data="buy")],
    [InlineKeyboardButton(text="Как выкладывать в Full HD", callback_data="hd")],
    [InlineKeyboardButton(text="Профиль", callback_data="profile")],
])

@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    name = f"@{user.username}" if user.username else user.first_name
    text = f"Привет, {name}!"
    try:
        await message.answer_photo(FSInputFile(LOGO), caption=text, reply_markup=main_kb)
    except Exception:
        await message.answer(text, reply_markup=main_kb)

@dp.callback_query(F.data == "hd")
async def hd(call: CallbackQuery):
    await call.message.answer(HD_TEXT)
    await call.answer()

@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    await call.message.answer(f"Твой ID: {call.from_user.id}")
    await call.answer()

@dp.callback_query(F.data == "buy")
async def buy(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я оплатил", callback_data="paid")],
    ])
    await call.message.answer(
        f"Тутор на качество: {PRICE}₽\n\n"
        f"Переведи {PRICE}₽:\n{PAY_INFO}\n\n"
        "Потом нажми «Я оплатил» и пришли скрин чека.",
        reply_markup=kb,
    )
    await call.answer()

@dp.callback_query(F.data == "paid")
async def paid(call: CallbackQuery):
    await call.message.answer("Пришли скриншот чека одним сообщением.")
    await call.answer()

@dp.message(F.photo | F.document)
async def receipt(message: Message):
    if message.from_user.id == ADMIN_ID:
        return
    user = message.from_user
    name = f"@{user.username}" if user.username else user.first_name
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Подтвердить", callback_data=f"ok:{user.id}"),
        InlineKeyboardButton(text="Отклонить", callback_data=f"no:{user.id}"),
    ]])
    await message.copy_to(ADMIN_ID)
    await bot.send_message(ADMIN_ID, f"Чек от {name} (ID {user.id})", reply_markup=kb)
    await message.answer("Чек отправлен, жди подтверждения.")

@dp.callback_query(F.data.startswith("ok:"))
async def approve(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return await call.answer()
    user_id = int(call.data.split(":")[1])
    await bot.send_message(user_id, TUTOR_TEXT)
    await call.message.edit_text("Подтверждено, тутор отправлен.")
    await call.answer()

@dp.callback_query(F.data.startswith("no:"))
async def reject(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return await call.answer()
    user_id = int(call.data.split(":")[1])
    await bot.send_message(user_id, "Оплата не подтверждена. Напиши в поддержку.")
    await call.message.edit_text("Отклонено.")
    await call.answer()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
