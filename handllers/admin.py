from aiogram import types, Router
from aiogram.types import FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from stateMachine import *
from buttone.adminKB import admin_kb
import db


router = Router()


@router.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'в меню':
        await message.answer("Что вы хотите заказать?", reply_markup=admin_kb)
        await state.set_state(UserMenu.menu)
    elif str(message.text).lower() == 'получить список всех пользователей':
        db.get_all_data()
        data = FSInputFile('exported_data.xlsx')
        await message.answer_document(data)
        await state.set_state(UserState.admin)

