from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from states.state import CategoryInfo
from keyboards.inline import *


@dp.callback_query_handler(text="add_category", state='*')
async def add_category(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await db.add_category(call.message.text)
