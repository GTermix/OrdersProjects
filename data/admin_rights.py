from data.config import ADMINS


async def make_admins_forever(db):
    admins_list = await db.get_all_admins()
    for admin_ in admins_list:
        ADMINS.append(str(admin_["telegram_id"]))
