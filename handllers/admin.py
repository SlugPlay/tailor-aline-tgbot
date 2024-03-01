from aiogram import types, Router
from aiogram.types import FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from stateMachine import *
import db

router = Router()


@router.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'в меню':
        kb = [
            [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
            [types.KeyboardButton(text="Хочу заказать низ Юбка")],
            [types.KeyboardButton(text="Хочу заказать низ Брюки")],
            [types.KeyboardButton(text="Связаться с менеджером")],
            [types.KeyboardButton(text="Зарегистрироваться заново")],
            [types.KeyboardButton(text="Вернуться в панель админа")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Что вы хотите заказать?", reply_markup=keyboard)
        await state.set_state(UserMenu.menu)
    elif str(message.text).lower() == 'получить список всех пользователей':
        db.get_all_data()
        data = FSInputFile('exported_data.xlsx')
        await message.answer_document(data)
        await state.set_state(UserState.admin)