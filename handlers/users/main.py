from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import ProductInfo
from keyboards.inline import *


@dp.callback_query_handler(text="add_category", state='*')
async def add_category(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await db.add_category(call.message.text)


@dp.message_handler(commands=["add_product"])
async def product(message: types.Message):
    await message.answer("Masulot nomini kiriting")
    await ProductInfo.title.set()


@dp.message_handler(state=ProductInfo.title)
async def product_title(message: types.Message, state: FSMContext):
    await state.update_data({"title": message.text})
    await message.answer("Mahsulot haqida qo'shimcha (to'liqroq) ma'lumot yozing")
    await ProductInfo.next()


@dp.message_handler(state=ProductInfo.desc)
async def product_desc(message: types.Message, state: FSMContext):
    await state.update_data({"desc": message.text})
    await message.answer("Mahsulot rasmini yuboring")
    await ProductInfo.next()


@dp.message_handler(content_types="photo", state=ProductInfo.picture)
async def product_photo(message: types.Message, state: FSMContext)
    await state.update_data({"picture": message.photo[-1].file_id})
    await message.answer("Mahsulot narxini kiriting")
    await ProductInfo.next()


@dp.message_handler(state=ProductInfo.price)
async def product_price(message: types.Message, state:FSMContext):
    await state.update_data({"price": float(message.text)})
    await message.answer("Bu mahsulotlar uchun chegirmalar mavjudmi bo'lsa kiriting foizini kitiing misol 25 yo'q bo'lsa 0 ni")
    await ProductInfo.next()


