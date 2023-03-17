from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


async def cats():
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_category()
    for cat in c1:
        categories.insert(InlineKeyboardButton(cat[1], callback_data=cat[1]))
    categories.add(InlineKeyboardButton("➕ Kategoriya qo'shish", callback_data="add_category"))
    return categories


def kats():
    cat = InlineKeyboardMarkup()
    cat.row(InlineKeyboardButton("Qo'shish", callback_data="add_cat"),
            InlineKeyboardButton("O'chirish", callback_data="del_cat"))
    return cat


def product():
    cat = InlineKeyboardMarkup()
    cat.row(InlineKeyboardButton("Qo'shish", callback_data="add_pro"),
            InlineKeyboardButton("O'chirish", callback_data="del_pro"))
    return cat


async def prod():
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_product()
    if c1:
        for cat in c1:
            categories.insert(InlineKeyboardButton(cat[1], callback_data=cat[1]))
    categories.add(InlineKeyboardButton("➕ Mahsulot qo'shish", callback_data="add_product"))
    return categories
