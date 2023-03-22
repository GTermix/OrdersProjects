from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.message_handler(text="Bosh menyu", state='*')
async def back_to_main(message: M):
    await message.answer("Asosiy menyudasiz", reply_markup=main_markup(message.from_user.id))
    await MainState.command.set()


@dp.message_handler(commands=["set_admin"], state='*')
async def admins(message: M):
    admins_list = await db.get_all_admins()
    for admin_ in admins_list:
        if admin_["telegram_id"] == message.from_user.id:
            await message.answer("Siz adminsiz funksional yangilanish uchun /start buyrug'ini bering "
                                 "yoki tugmani bosing", reply_markup=restart)
            ADMINS.append(str(admin_["telegram_id"]))
            break
    else:
        await message.answer(
            "Sizni admin qila olmayman chunki siz mening ma'lumotlar bazamda admin sifatida kiritilmagansiz ")


@dp.message_handler(commands=['del_admin'], chat_id=ADMINS[0], state='*')
async def del_admin(message: M):
    await message.answer("Menga Adminlikdan ozod qilmoqchi bo'lgan admin id sini yuboring")
    await AdminRight.del_admin.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=AdminRight.del_admin)
async def rights(message: M, state: FSMContext):
    await db.delete_admin(int(message.text))
    ADMINS.remove(message.text)
    await message.answer(
        "Admin adminlikdan ozod qilindi admin shunchaki /start bosishi kerak. Start bosishi haqida aldovchi xabar yuborildi")
    await bot.send_message(int(message.text), "Botda yangilanish iltimos funksiyanal yangilanish uchun /start bosing",
                           reply_markup=restart)
    await state.finish()


@dp.message_handler(commands=["up_admin"], chat_id=ADMINS, state='*')
async def admin(message: M):
    await message.answer("Menga yangi admin id sini yuboring", reply_markup=back1())
    await AdminRight.send_id.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=AdminRight.send_id)
async def rights(message: M, state: FSMContext):
    await db.add_admin(int(message.text))
    await message.answer("Yangi admin bazaga qo'shildi. Yangi admin /set_admin kommandasini berganda "
                         "adminlar safiga qo'shiladi")
    await state.finish()


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
        await message.answer("Savatcha bo'limidasiz", reply_markup=back1())
        msg = "Savatchangizdagi, buyurtma qilgan mahsulotlaringiz:\n\n\n"
        c = await db.get_data_from_order_table(message.from_user.id)
        my_cart = ''
        total_price = 0
        if c:
            for k in c:
                my_cart_data = await db.get_data_from_product_cart(k['product_id'])
                price = k['count']
                for j in my_cart_data:
                    my_cart += f"Mahsulot nomi: {j['title']}\nMahsulotlar soni {price}\nMahsulotlar narxi(chegirmalar bilan): " \
                               f"{(float(j['price']) * ((100 - j['discount']) / 100)) * price} so'm\n\n"
                    total_price += (float(j['price']) * ((100 - j['discount']) / 100)) * price
            ans = msg + my_cart + f"Jami to'lov summasi: {total_price} so'm"
            await message.answer(ans, reply_markup=cart_menu)
        else:
            ans = f"Hozircha savatchangiz bo'sh harid qiling va savatchangizni to'ldiring"
            await message.answer(ans)
        await state.finish()
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


@dp.callback_query_handler(text="del_cart")
async def del_cart(call: types.CallbackQuery):
    await db.delete_order(call.from_user.id)
    await call.message.delete()
    await call.message.answer("Savatchangiz tozalandi kerakli narsalaringiz bo'lsa buyurtma berishingiz mumkin",
                              reply_markup=back1())