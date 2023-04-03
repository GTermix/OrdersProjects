from loader import dp, bot
from data.config import CHANNELS, ADMINS
from utils.misc import subscription
from aiogram import types
from keyboards.default.main import main_markup
from states.state import MainState
from keyboards.default.main import main_markup
from keyboards.inline.subscription import check_subs


@dp.message_handler(commands=['add_channel'], state="*")
async def add_channel_to_list(message: types.Message):
    await message.answer("Qo'shilish majburiy bo'lgan kanal nomini yuboring")


@dp.callback_query_handler(text="check_subs", state='*')
async def checker(call: types.CallbackQuery):
    await call.answer()
    final_status = True
    result = list()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status

        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            result.append(invite_link)

    if final_status:
        await call.message.delete()
        msg = f"Assalomu alaykum, xush kelibsiz\n👤 <b><a href=\"tg://user?id={call.from_user.id}\">" \
              f"{call.from_user.full_name}</a></b>!" \
              f"\nBotimizdan foydalanishingiz mumkin. Tugmalardan foydalanib menga xabar yuboring 🔽"
        await call.message.answer(msg, reply_markup=main_markup(call.from_user.id))
        await MainState.command.set()
    else:
        await call.message.delete()
        await call.message.answer("Quyidagi kanallarimizga obuna bo'lmagansiz obuna bo'ling 👇",
                                  disable_web_page_preview=True, reply_markup=check_subs(result))
