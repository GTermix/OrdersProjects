import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from states.state import *
from keyboards.default.main import *


@dp.message_handler(lambda message: message.text != "Bosh menyu", content_types=["any"], state=SendToUsers.msg)
async def send_msg(message: types.Message, state: FSMContext):
    await message.answer(
        "Random orqali yuborilsinmi. Random orqali aksiyalar qilishingiz mumkin misol uchun 100 ta odam uchun siz "
        "yozgan xabarni yuborishingiz mumkin, "
        "bunda ular tasodifiy tanlanadi", reply_markup=confirmation)
    a = message.message_id
    b = message.chat.id
    await state.update_data({"chat_id": b, "msg_id": a})
    await SendToUsers.next()


@dp.message_handler(lambda message: message.text != "Bosh menyu", state=SendToUsers.random_send)
async def send_msg(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    if msg == "Ha":
        count = await db.count_users()
        await message.answer(f"Nechta odamga yuborilsin sonini kiriting hozirda bot da {count} ta foydalanuvchi bor")
        await SendToUsers.next()
    elif msg == "Yo'q":
        user_ids = await db.get_data_from_user_id()
        if user_ids:
            for i in user_ids:
                await message.answer(f"Xabar [Foydalanuvchiga yetkazildi](tg://user?id={i['telegram_id']})",
                                     parse_mode="markdown")
                await bot.copy_message(i['telegram_id'], data.get("chat_id"), data.get("msg_id"))
                await asyncio.sleep(0.05)
            else:
                await message.answer("Xabar barcha foydalanuvhilarga yetkazildi", reply_markup=back1())
        else:
            await message.answer("Hozircha bot da yetarlicha odam yo'q", reply_markup=back1())
    else:
        await message.answer("Iltimos tugmalar orqali buyruq bering")


@dp.message_handler(lambda message: message.text.isdigit(), state=SendToUsers.random_num)
async def ran_num(message: types.Message, state: FSMContext):
    sent_users = []
    numbers = int(message.text)
    data = await state.get_data()
    user_ids = await db.get_data_from_user_id()
    if user_ids and len(user_ids) > numbers:
        while not numbers == 0:
            random_user = random.choice(user_ids)
            if random_user not in sent_users:
                print(random_user['telegram_id'])
                await message.answer(f"Xabar [Foydalanuvchiga yetkazildi](tg://user?id={random_user['telegram_id']})",
                                     parse_mode="markdown")
                await bot.copy_message(random_user['telegram_id'], data.get("chat_id"), data.get("msg_id"))
                await asyncio.sleep(0.05)
                sent_users.append(random_user)
            else:
                numbers += 1
            numbers -= 1
        else:
            await message.answer("Xabar yetkazildi")
            sent_users.clear()
            await message.answer("Asosiy menyudasiz", reply_markup=main_markup(message.from_user.id))
            await MainState.command.set()
    else:
        await message.answer("Hozircha bot da yetarlicha odam yo'q", reply_markup=back1())
