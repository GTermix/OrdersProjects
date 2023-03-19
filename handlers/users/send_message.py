from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from states.state import SendToUsers
from keyboards.default.main import *


@dp.message_handler(content_types=["any"], state=SendToUsers.msg)
async def send_msg(message: types.Message, state: FSMContext):
    await message.answer(
        "Random orqali yuborilsinmi. Random orqali aksiyalar qilishingiz mumkin misol uchun 100 ta odam uchun siz "
        "yozgan xabarni yuborishingiz mumkin, "
        "bunda ular tasodifiy tanlanadi", reply_markup=confirmation)
    a = message.message_id
    b = message.chat.id
    await state.update_data({"chat_id": b, "msg_id": a})
    await SendToUsers.next()


@dp.message_handler(state=SendToUsers.random_send)
async def send_msg(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    if msg == "Ha":
        await message.answer("a")
    elif msg == "Yo'q":
        user_ids = await db.get_data_from_user_id()
        if user_ids:
            for i in user_ids:
                await bot.copy_message(i['telegram_id'], data.get("chat_id"), data.get("msg_id"))
            else:
                await message.answer("Xabar barcha foydalanuvhilarga yetkazildi", reply_markup=back1())
        else:
            await message.answer("Hozircha bot da yetarlicha odam yo'q", reply_markup=back1())
    else:
        await message.answer("Iltimos tugmalar orqali buyruq bering")
