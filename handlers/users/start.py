from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.main import main_markup
from states.state import MainState
from data.config import CHANNELS
from keyboards.inline.subscription import check_button


@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"➡️ <a href='{invite_link}'><b>{chat.title}</b></a>\n"
    await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n\n"
                         f"{channels_format}",
                         reply_markup=check_button,
                         disable_web_page_preview=True)
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
