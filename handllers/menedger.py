from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from tailor_aline_tgbot.config import bot
from tailor_aline_tgbot.stateMachine import *

from tailor_aline_tgbot import db

router = Router()


@router.message(StateFilter(UserReg.problem))
async def problem(message: types.Message, state: FSMContext):
    global all_user_data
    if str(message.text).lower() == 'назад':
        kb = [
            [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
            [types.KeyboardButton(text="Хочу заказать низ Юбка")],
            [types.KeyboardButton(text="Хочу заказать низ Брюки")],
            [types.KeyboardButton(text="Связаться с менеджером")],
            [types.KeyboardButton(text="Зарегистрироваться заново")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Что вы хотите заказать?", reply_markup=keyboard)
        await state.set_state(UserMenu.menu)
    else:
        admin_data = db.get_admin_data()
        for i in admin_data:
            await bot.send_message(i,
                                   "Новое обращение с вопросом!\nПользователь номер: {}\nНомер телефона: {}\nИмя: {}\nФамилия: {}\nВозраст: {}\nРегион: {}\nРазмер: {}\n".format(
                                       all_user_data[0], all_user_data[1], all_user_data[2], all_user_data[3],
                                       all_user_data[4], all_user_data[5], all_user_data[6]))
            if all_user_data[7][:-3] == 'pic':
                await bot.send_photo(i, all_user_data[7][:-4], caption='Фото спереди:')
            else:
                await bot.send_document(i, all_user_data[7][:-4], caption='Фото спереди:')
            if all_user_data[8][:-3] == 'pic':
                await bot.send_photo(i, all_user_data[8][:-4], caption='Фото сзади:')
            else:
                await bot.send_document(i, all_user_data[8][:-4], caption='Фото сзади:')
            if all_user_data[9][:-3] == 'pic':
                await bot.send_photo(i, all_user_data[9][:-4], caption='Фото в профиль:')
            else:
                await bot.send_document(i, all_user_data[9][:-4], caption='Фото в профиль:')
            await bot.send_message(i, 'Текст проблемы:')
            await bot.forward_message(i, message.chat.id, message.message_id)
        kb = [
            [types.KeyboardButton(text="В меню")],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Менеджер свяжется с вами в течении 1 часа', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
