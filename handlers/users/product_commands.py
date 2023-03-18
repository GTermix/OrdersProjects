from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.callback_query_handler(text="add_pro")
async def product_fun(call: types.CallbackQuery):
    cat = await cats(call.from_user.id)
    await call.message.delete()
    await call.message.answer("Mahsulot kategoriyasini tanlang", reply_markup=cat)
    await ProductInfo.cat_id.set()


@dp.callback_query_handler(state=ProductInfo.cat_id)
async def set_category_id(call: types.CallbackQuery, state: FSMContext):
    cat_id = await db.get_data_from_category_id(call.data)
    await state.update_data({"cat_id": cat_id})
    await call.message.answer("Masulot nomini kiriting", reply_markup=None)
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
async def product_photo(message: types.Message, state: FSMContext):
    await state.update_data({"photo": message.photo[-1].file_id})
    await message.answer("Mahsulot narxini kiriting")
    await ProductInfo.next()


@dp.message_handler(state=ProductInfo.price)
async def product_price(message: types.Message, state: FSMContext):
    await state.update_data({"price": float(message.text)})
    await message.answer(
        "Bu mahsulotlar uchun chegirmalar mavjudmi bo'lsa kiriting foizini kiting.\nMisol 25 yo'q bo'lsa 0 ni")
    await ProductInfo.next()


@dp.message_handler(state=ProductInfo.discount)
async def product_discount(message: types.Message, state: FSMContext):
    await state.update_data({"discount": float(message.text)})
    data = await state.get_data()
    cat_title = await db.get_data_from_category_title(data.get('cat_id'))
    await message.answer(
        "Ma'lumotlar to'g'rimi, agar keyinchalik xato topilsa keyinchalik bu mahsulotni yo'q qilishingiz mumkin")
    product_info = f"Mahsulot kategoriyasi: {cat_title}\n\n" \
                   f"Mahsulot nomi: {data.get('title')}\n\n" \
                   f"Mahsulot tavsifi: {data.get('desc')}\n\n" \
                   f"Mahsulot narxi: {data.get('price')} so'm\n\n" \
                   f"Chegirmalar: {data.get('discount')} %"
    await message.answer_photo(photo=data.get('photo'), caption=product_info, reply_markup=confirm)
    await ProductInfo.next()


@dp.callback_query_handler(text="yes", state=ProductInfo.confirmed)
async def add_to_products(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Mahsulot bazaga qo'shildi")
    await call.message.delete()
    data = await state.get_data()
    await db.add_product(data.get("title"), data.get("desc"), data.get("cat_id"), data.get("photo"), data.get("price"),
                         data.get("discount"))
    await state.finish()
    await call.message.answer("Mahsulotlar panelidasiz kerakli buyruqlarni tugmalar orqali bering",
                              reply_markup=back1())
    await call.message.answer("Kerakli bo'limni talang", reply_markup=product())
    await AddCategory.title.set()


@dp.callback_query_handler(text="no", state=ProductInfo.confirmed)
async def cancel_products(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Mahsulotlar panelidasiz kerakli buyruqlarni tugmalar orqali bering",
                              reply_markup=back1())
    await call.message.answer("Kerakli bo'limni talang", reply_markup=product())
    await state.finish()
    await AddCategory.title.set()
