from loader import dp, db, bot
from aiogram import types


def get_cats(message: types.Message):
    user = await db.add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )
