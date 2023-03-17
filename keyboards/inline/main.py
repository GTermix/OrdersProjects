from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


async def cats():
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_user()
    for cat in c1:
        print(cats)
    categories.add(InlineKeyboardButton("➕ Kategoriya qo'shish", callback_data="add_category"))
print(catego)