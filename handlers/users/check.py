from loader import dp, bot
from data.config import CHANNELS, ADMINS
from utils.misc import subscription
from aiogram import types
from keyboards.default.main import main_markup
from states.state import MainState
from keyboards.default.main import main_markup
from keyboards.inline.subscription import check_button


@dp.callback_query_handler(text="check_subs", state='*')
async def checker(call: types.CallbackQuery):
    await call.answer()
    final_status = True
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status
            result += f"✅ <b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"

        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            result += f"❌ <a href='{invite_link}'><b>{channel.title}</b></a> kanaliga obuna bo'lmagansiz.\n\n"

    if final_status:
        name = call.from_user.username
        await bot.send_message(chat_id=ADMINS[0], text=f"@{name} botga qo'shildi")
        await call.message.answer(f"Xush kelibsiz! @{name}", reply_markup=main_markup(str(call.from_user.id)))
        await MainState.command.set()
        await call.message.delete()
        msg = f"Salom xush kelibsiz\n👤 <b>{call.from_user.full_name}</b>!\nE'lon berishni hohlaysizmi? 🔽"
        await call.message.answer(msg, reply_markup=main_markup(call.from_user.id))
    else:
        await call.message.delete()
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=check_button)
