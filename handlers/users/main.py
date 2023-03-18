from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.message_handler(text="Orqaga qaytish")
async def back1a(message: M, state: FSMContext):
    await state.finish()
    await message.answer("Bosh menyudasiz kerakli bo'limingizni tanlang",
                         reply_markup=main_markup(message.from_user.id))
    await MainState.command.set()


@dp.message_handler(state=MainState.command)
async def main_menu_panel(message: M, state: FSMContext):
    msg = message.text
    cat_markup = await cats(message.from_user.id)
    if msg == "Buyurtma berish":
        await message.answer("Buyurtma berish uchun kategoriya tanlang", reply_markup=cat_markup)
    elif msg == "Savatcha":
        await message.answer("Savatcha bo'limidasiz")
    elif msg == "Bog'lanish":
        await message.answer("Admin bilan bog'lanish")
    elif msg == "Kategoriya paneli":
        await message.answer("Kategoriyalar panelidasiz kerakli buyruqlaringizni yugmalar orqali bering",
                             reply_markup=back1())
        await message.answer("Kerakli bo'limni tanlang", reply_markup=kats())
        await state.finish()
    elif msg == "Mahsulot paneli":
        await message.answer("Mahsulotlar panelidasiz kerakli buyruqlarni tugmalar orqali bering", reply_markup=back1())
        await message.answer("Kerakli bo'limni talang", reply_markup=product())
        await state.finish()
    elif msg == "Xabar yuborish":
        await message.answer("Aynan kimga xabar yuborishni xoxlaysiz")
    else:
        await message.answer("Menga tugmalar orqali buyruq bering")
