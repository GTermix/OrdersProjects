from aiogram import types
from aiogram.types.message import ContentTypes
from aiogram.utils import executor
from loader import db, dp, bot

shipping_options = [
    types.ShippingOption(id='instant', title='WorldWide Teleporter').add(types.LabeledPrice('Teleporter', 10000)),
    types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 30000)),
]


def get_prices(price_):
    prices = [
        types.LabeledPrice(label='Mahsulotlar narxi', amount=price_)
    ]
    return prices
