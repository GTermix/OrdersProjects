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


class DeleteFromDB(StatesGroup):
    confirmation = State()
    deletion = State()


class BackupState(StatesGroup):
    base = State()
    copy = State()
    confirm = State()


class PlaceOrder(StatesGroup):
    category = State()
    product = State()
    wait = State()
    last = State()


class Cart(StatesGroup):
    command = State()


class SendToUsers(StatesGroup):
    msg = State()
    random_send = State()
    random_num = State()