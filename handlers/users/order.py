from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.callback_query_handler(state=PlaceOrder.category)
async def cat_of_order(call: types.CallbackQuery, state: FSMContext):
    mark1 = await db.get_data_from_category_id(call.data)
    markup = await prod(mark1)
    await call.message.edit_text("Mahsulotni tanlang", reply_markup=markup)
