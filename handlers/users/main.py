from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.message_handler(state=MainState.command)
async def main_menu_panel(message: M, state: FSMContext):
    msg = message.text
    cat_markup = await cats()
    if msg == "Buyurtma berish":
        await message.answer("Buyurtmalar menyusidasiz", reply_markup=back1())
        await message.answer("Buyurtma berish uchun kategoriya tanlang", reply_markup=cat_markup)
        await state.finish()
        await PlaceOrder.category.set()
    elif msg == "Savatcha":
        msg = "Savatchangizdagi, buyurtma qilgan mahsulotlaringiz:\n\n\n"
        c = await db.get_data_from_order_table(message.from_user.id)
        my_cart = ''
        total_price = 0
        if c:
            for k in c:
                my_cart_data = await db.get_data_from_product_cart(k['product_id'])
                price = k['count']
                for j in my_cart_data:
                    my_cart += f"Mahsulot nomi: {j['title']}\nMahsulotlar soni {price}\nMahsulotlar narxi: " \
                               f"{(float(j['price']) * ((100 - j['discount']) / 100)) * price} so'm\n\n"
                    total_price += (float(j['price']) * ((100 - j['discount']) / 100)) * price
            ans = msg + my_cart + f"Jami to'lov summasi: {total_price} so'm"
        else:
            ans = f"Hozircha savatchangiz bo'sh harid qiling va savatchangizni to'ldiring"
        await message.answer(ans)
    elif msg == "Bog'lanish":
        await message.answer("Admin bilan bog'lanish", reply_markup=contact_with)
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
        await message.answer("Xabarni kiriting.\nXabaringiz aynan qanday bo'lsa shunday yetkaziladi",
                             reply_markup=back1())
        await SendToUsers.msg.set()
    else:
        await message.answer("Menga tugmalar orqali buyruq bering")


@dp.message_handler(text="Bosh menyu", state='*')
async def back_to_main(message: M):
    await message.answer("Asosiy menyudasiz", reply_markup=main_markup(message.from_user.id))
    await MainState.command.set()
