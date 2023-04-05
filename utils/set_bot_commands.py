from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )


async def set_default_admin_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("add_channel", "Botga yangi kanal ulash"),
            types.BotCommand("up_admin", "Yangi admin tayinlash"),
            types.BotCommand("del_admin", "Adminni adminlidan ozodmqilish")
        ]
    )
