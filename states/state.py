from aiogram.dispatcher.filters.state import State, StatesGroup


class CategoryInfo(StatesGroup):
    title = State()


class ProductInfo(StatesGroup):
    cat_id = State()
    title = State()
    desc = State()
    price = State()
    picture = State()
