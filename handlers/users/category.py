from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message as M
from aiogram.dispatcher import FSMContext
from states.state import *
from keyboards.inline.main import *
from keyboards.default.main import *


@dp.callback_query_handler(text="backup")
async def backup_category(call: types.CallbackQuery):
    cat = await cats(call.from_user.id)
    await call.message.edit_text("Zaxiralamoqchi bo'lgan kategoriyangizni tanlang", reply_markup=cat)
    await BackupState.base.set()


@dp.callback_query_handler(state=BackupState.base)
async def backup_base(call: types.CallbackQuery, state: FSMContext):
    cat_id = await db.get_data_from_category_id(call.data)
    await state.update_data({"base": cat_id, "base_title": call.data})
    cat = await cats(call.from_user.id)
    await call.message.edit_text("Qaysi kategoriyaga zaxiralamoqchisiz", reply_markup=cat)
    await BackupState.next()


@dp.callback_query_handler(state=BackupState.copy)
async def backup_copy(call: types.CallbackQuery, state: FSMContext):
    cat_id = await db.get_data_from_category_id(call.data)
    await state.update_data({"copy": cat_id, "copy_title": call.data})
    await call.message.delete()
    data = await state.get_data()
    ans = f"Haqiqatdan ham <b>{data.get('base_title')}</b> kategoriyasidagi barcha mahsulotlarni {data.get('copy_title')} " \
          f"ko'chirish(zaxiralash)ni xoxlaysizmi"
    await call.message.answer(ans, reply_markup=confirm)
    await BackupState.next()


@dp.callback_query_handler(text="no", state=BackupState.confirm)
async def backup_base(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Bosh menyudasiz", reply_markup=main_markup(call.from_user.id))
    await state.finish()
    await MainState.command.set()


@dp.callback_query_handler(text="yes", state=BackupState.confirm)
async def backup_base(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.backup_products_to_category(data.get('base'), data.get('copy'))
    await call.message.delete()
    await call.message.answer(f"{data.get('base_title')} kategoriyasidagi hamma ma'lumotlar {data.get('copy_title')} "
                              f"kategoriyasiga ko'chirildi")


@dp.callback_query_handler(text="add_cat")
async def add_category(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await AddCategory.title.set()


@dp.callback_query_handler(text="del_cat")
async def add_category(call: types.CallbackQuery):
    cat = await cats(call.from_user.id)
    await call.message.edit_text("O'chirish uchun kategoriyani tanlang", reply_markup=cat)
    await DeleteFromDB.confirmation.set()


@dp.callback_query_handler(state=DeleteFromDB.confirmation)
async def confirm_del(call: types.CallbackQuery, state: FSMContext):
    cat_id = await db.get_data_from_category_id(call.data)
    await state.update_data({"id": cat_id})
    await call.message.edit_text(
        f"Ushbu kategoriyani o'chirishga ishonchingiz komilmi ?\n\n<i><b>{call.data}</b></i>\n\nO'chirilgan kategoriyani qayta tiklab bo'lmaydi ammo "
        "qayta yaratish mumkin\n\n<b>KATEGORIYA O'CHIRILGANDA KATEGORIYA ICHIDAGI MAHSULOTLAR HAM O'CHADI</b>\n\nAgar "
        "mahsulotlarni saqlab qolishni istasangiz uni boshqa kategoriyaga zaxiralashingiz mumkin", reply_markup=confirm)
    await DeleteFromDB.next()


@dp.callback_query_handler(text="yes", state=DeleteFromDB.deletion)
async def confirm_del(call: types.CallbackQuery, state: FSMContext):
    id_cat = await state.get_data()
    await db.delete_category(id_cat.get("id"))
    await call.message.delete()
    await call.message.answer("Kategoriya o'chirildi", reply_markup=main_markup(call.from_user.id))
    await state.finish()
    await MainState.command.set()


@dp.message_handler(state=AddCategory.title)
async def adding_category(message: types.Message, state: FSMContext):
    await db.add_category(message.text)
    await message.answer("Yangi kategoriya qo'shildi", reply_markup=back1())
    await message.answer("Kerakli bo'limni tanlang", reply_markup=kats())
    await state.finish()
