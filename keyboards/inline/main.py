from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.postgres import get_data_from_category

categories = InlineKeyboardMarkup()

for cats in db.get_data_from_category():
    print(cats)
categories.add(InlineKeyboardButton("➕ Kategoriya qo'shish",callback_data="add_category"))