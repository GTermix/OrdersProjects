from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    command = State()


class AddCategory(StatesGroup):
    title = State()


class ProductInfo(StatesGroup):
    cat_id = State()
    title = State()
    desc = State()
    picture = State()
    price = State()
    discount = State()
    confirmed = State()
