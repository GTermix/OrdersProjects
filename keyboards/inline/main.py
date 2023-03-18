from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import ADMINS

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


async def cats(chatId):
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_category()
    for cat in c1:
        categories.insert(InlineKeyboardButton(cat[1], callback_data=cat[1]))
    # if str(chatId) in ADMINS:
    #     categories.add(InlineKeyboardButton("➕ Kategoriya qo'shish", callback_data="add_category"))
    return categories


def kats():
    cat = InlineKeyboardMarkup()
    cat.row(InlineKeyboardButton("Qo'shish", callback_data="add_cat"),
            InlineKeyboardButton("O'chirish", callback_data="del_cat"))
    cat.row(InlineKeyboardButton("Kategoriyani zaxiralash", callback_data="backup"))
    return cat


def product():
    cat = InlineKeyboardMarkup()
    cat.row(InlineKeyboardButton("Qo'shish", callback_data="add_pro"),
            InlineKeyboardButton("O'chirish", callback_data="del_pro"))
    return cat


async def prod(cat_id):
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_product_title(cat_id=cat_id)
    if c1:
        for cat in c1:
            categories.insert(InlineKeyboardButton(cat['title'], callback_data=cat["title"]))
    return categories
