from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from tailor_aline_tgbot.stateMachine import *
from buttone.adminKB import admin_kb
router = Router()


@router.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'в меню':
        await message.answer("Что вы хотите заказать?", reply_markup=admin_kb)
        await state.set_state(UserMenu.menu)
