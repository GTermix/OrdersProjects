from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import ADMINS


def main_markup(chatId):
    main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main.add(KeyboardButton("Buyurtma berish"))
    main.row(KeyboardButton("Savatcha"), KeyboardButton("Bog'lanish"))
    if str(chatId) in ADMINS:
        main.insert(KeyboardButton("Kategoriya paneli"))
        main.insert(KeyboardButton("Mahsulot paneli"))
        main.insert(KeyboardButton("Xabar yuborish"))
    return main


def send_messages():
    rmk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rmk.add(KeyboardButton("Foydalanuvchilarga xabar yuborish"))
    rmk.add(KeyboardButton("Guruh(kanal)larga xabar yuborish"))
    return rmk


def back1():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton("Bosh menyu"))
    return m


confirmation = ReplyKeyboardMarkup(resize_keyboard=True)
confirmation.insert(KeyboardButton("Ha"))
confirmation.insert(KeyboardButton("Yo'q"))
