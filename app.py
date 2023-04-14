from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.admin_rights import make_admins_forever


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()
    await db.create_table_category()
    await db.create_table_product()
    await db.create_table_order()
    await db.create_table_admins()
    await make_admins_forever(db)

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
