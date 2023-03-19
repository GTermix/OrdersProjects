from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *

summa = ''


@dp.callback_query_handler(text="back_cat", state=PlaceOrder.product)
async def back_to_cat(call: types.CallbackQuery):
    cat_markup = await cats()
    await call.message.edit_text("Buyurtma berish uchun kategoriya tanlang", reply_markup=cat_markup)
    await PlaceOrder.category.set()


@dp.callback_query_handler(state=PlaceOrder.category)
async def cat_of_order(call: types.CallbackQuery, state: FSMContext):
    mark1 = await db.get_data_from_category_id(call.data)
    markup = await prod(mark1)
    c1 = await db.get_data_from_product_title(cat_id=mark1)
    if c1:
        await call.message.edit_text("Mahsulotni tanlang", reply_markup=markup)
        await state.update_data({"cat_id": mark1})
    else:
        await call.message.edit_text(f"Hozircha {call.data} kategoriyasida mahsulotlar mavjud emas",
                                     reply_markup=markup)
    await PlaceOrder.next()


@dp.callback_query_handler(state=PlaceOrder.product)
async def back_to_cat(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pro_id = await db.get_data_from_product_id(data.get("cat_id"), call.data)
    await state.update_data({"pro_id": pro_id})
    info = await db.get_data_from_product_all(data.get("cat_id"), pro_id)
    info = info[0]
    if float(info.get('discount')) == 0:
        capt = f"Mahsulot nomi: {info.get('title')}\n\n" \
               f"Mahsulot haqida ma'lumot: {info.get('description')}\n\n" \
               f"Mahsulotga chegirma: {info.get('discount')} %\n\n" \
               f"Mahsulot narxi: {float(info.get('price'))} so'm "
    else:
        capt = f"Mahsulot nomi: {info.get('title')}\n\n" \
               f"Mahsulot haqida ma'lumot: {info.get('description')}\n\n" \
               f"Mahsulotga chegirma: {info.get('discount')} %\n\n" \
               f"Mahsulot narxi: <del>{float(info.get('price'))} so'm</del> " \
               f"→ {float(info.get('price')) * ((100 - info.get('discount')) / 100)} so'm\n\n"
    await call.message.delete()
    await call.message.answer_photo(info.get('image_url'), capt, reply_markup=to_cart)
    await PlaceOrder.next()


@dp.callback_query_handler(state=PlaceOrder.wait)
async def d(call: types.CallbackQuery, state: FSMContext):
    c = call.data
    cm = await state.get_data()
    if c == "to_cart":
        await call.message.delete()
        await call.message.answer(
            "Mahsulotdan qancha miqdorda olmoqchisiz ushbu tugmalar yordamida kiriting va bajarildini bosing. "
            "Shunchaki bajarildini bossangiz 1 ta saqlanadi", reply_markup=salary)
        await PlaceOrder.next()
    elif c == "back_to_pro":
        markup = await prod(cat_id=cm.get('cat_id'))
        c1 = await db.get_data_from_product_title(cat_id=cm.get('cat_id'))
        await call.message.delete()
        await call.message.answer("Mahsulotni tanlan", reply_markup=markup)
        await PlaceOrder.product.set()
    elif c == "back_to_cat":
        pass


@dp.callback_query_handler(text="done", state=PlaceOrder.last)
async def callme(call: types.CallbackQuery, state: FSMContext):
    global summa
    if not summa:
        summa = '1'
    cm = await state.get_data()
    await state.update_data({"count": summa})
    await call.message.edit_text(f"Bajarildi!\n{summa} ta mahsulot savatgchaga qo'shildi", reply_markup=None)
    await db.add_order(call.from_user.id, cm.get('pro_id'), summa)
    summa = ''


@dp.callback_query_handler(text="clear", state=PlaceOrder.last)
async def callme(call: types.CallbackQuery):
    global summa
    summa = "0"
    await call.message.edit_text(f"Buyurmoqchi bo'lgan mahsulotingiz soni: <b>{summa}</b> ta", reply_markup=salary)
    summa = ""


@dp.callback_query_handler(state=PlaceOrder.last)
async def callme(call: types.CallbackQuery):
    global summa
    summa += call.data
    await call.message.edit_text(f"Buyurmoqchi bo'lgan mahsulotingiz soni: <b>{summa}</b> ta", reply_markup=salary)
