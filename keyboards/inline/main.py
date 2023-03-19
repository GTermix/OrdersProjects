from loader import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import ADMINS

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


async def cats():
    categories = InlineKeyboardMarkup()
    c1 = await db.get_data_from_category()
    for cat in c1:
        categories.insert(InlineKeyboardButton(cat[1], callback_data=cat[1]))
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
    else:
        categories.add(InlineKeyboardButton("Orqaga", callback_data="back_cat"))
    return categories


to_cart = InlineKeyboardMarkup(row_width=1)
to_cart.add(InlineKeyboardButton("Savatchaga", callback_data="to_cart"))
to_cart.add(InlineKeyboardButton("Mahsulotlarga qaytish", callback_data="back_to_pro"))
to_cart.add(InlineKeyboardButton("Kategoriyalarga qaytish", callback_data="back_to_cat"))

salary = InlineKeyboardMarkup()
for i in range(1, 10):
    salary.insert(InlineKeyboardButton(str(i), callback_data=str(i)))
salary.add(InlineKeyboardButton("0", callback_data="0"))
salary.add(InlineKeyboardButton("🗑 Mahsulot sonini tozalash", callback_data="clear"))
salary.add(InlineKeyboardButton("✅ Bajarildi", callback_data='done'))

contact_with = InlineKeyboardMarkup()
contact_with.add(InlineKeyboardButton("Dasturchi", url="https://t.me/yuldashevb_0221"))
contact_with.add(InlineKeyboardButton("Admin", url="https://t.me/yuldoshev"))