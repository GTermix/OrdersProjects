from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.postgres import get_data_from_category

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))

categories = InlineKeyboardMarkup()

for cats in db.get_data_from_category():
    print(cats)
categories.add(InlineKeyboardButton("➕ Kategoriya qo'shish",callback_data="add_category"))