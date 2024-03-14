from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from stateMachine import *
from buttone.adminKB import admin_kb
import db
from aiogram.types import FSInputFile
from func import check_user

router = Router()


@router.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'получить список всех пользователей':
        db.get_all_data()
        data = FSInputFile('exported_data.xlsx')
        await message.answer_document(data)
        await state.set_state(UserState.admin)
    elif str(message.text).lower() == 'добавить пользователя в чёрный список':
        await message.answer('Введите номер телефона пользователя')
        await state.set_state(UserAdmin.ban)
    elif str(message.text).lower() == 'просмотреть информацию о пользователе':
        await message.answer('Введите номер телефона пользователя')
        await state.set_state(UserAdmin.checkUser)
    

@router.message(StateFilter(UserAdmin.ban))
async def ban(message: types.Message, state: FSMContext):
    phone_target = str(message.text)
    db.ban_user(phone_target)
    await message.answer('Пользователь успешно внесён в чёрный список', reply_markup=admin_kb)
    await state.set_state(UserState.admin)


@router.message(StateFilter(UserAdmin.checkUser))
async def ban(message: types.Message, state: FSMContext):
    phone_target = str(message.text)
    await check_user(message.chat.id, db.get_user(phone_target))
    await message.answer('Готово', reply_markup=admin_kb)
    await state.set_state(UserState.admin)