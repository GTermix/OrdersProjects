from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import ProductInfo, AddCategory
from keyboards.inline.main import confirm, cats


@dp.callback_query_handler(text="add_category")
async def add_category(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await AddCategory.title.set()


@dp.message_handler(state=AddCategory.title)
async def addcategory(message: types.Message):
    await db.add_category(message.text)
    await message.answer("Yangi kategoriya qo'shildi")


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
    product_info = f"Mahsulot kategoriyasi: {data.get('category')}\n\n" \
                   f"Mahsulot nomi: {data.get('title')}\n\n" \
                   f"Mahsulot tavsifi: {data.get('description')}\n\n" \
                   f"Mahsulot narxi: {data.get('price')} so'm\n\n" \
                   f"Chegirmalar mavjud emas {data.get('discount')} %"
    await message.answer_photo(photo=data.get('photo'), caption=product_info, reply_markup=confirm)
