from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductInfo(StatesGroup):
    cat_id = State()
    title = State()
    desc = State()
    picture = State()
    price = State()
    discount = State()
