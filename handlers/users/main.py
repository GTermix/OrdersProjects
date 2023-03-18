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
        await AddCategory.title.set()
        await state.finish()
    elif msg == "Mahsulot paneli":
        await message.answer("Mahsulotlar panelidasiz kerakli buyruqlarni tugmalar orqali bering", reply_markup=back1())
        await message.answer("Kerakli bo'limni talang", reply_markup=product())
        await AddCategory.title.set()
        await state.finish()
    elif msg == "Xabar yuborish":
        await message.answer("Aynan kimga xabar yuborishni xoxlaysiz")
    else:
        await message.answer("Menga tugmalar orqali buyruq bering")


@dp.callback_query_handler(text="add_cat")
async def add_category(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await AddCategory.title.set()


@dp.message_handler(state=AddCategory.title)
async def adding_category(message: types.Message, state: FSMContext):
    await db.add_category(message.text)
    await message.answer("Yangi kategoriya qo'shildi", reply_markup=back1())
    await message.answer("Kerakli bo'limni tanlang", reply_markup=kats())
    await state.finish()


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
    data = await state.get_data()
    await db.add_product(data.get("title"), data.get("desc"), data.get("cat_id"), data.get("photo"), data.get("price"),
                         data.get("discount"))
    await state.finish()
