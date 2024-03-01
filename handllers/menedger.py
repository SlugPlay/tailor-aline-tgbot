from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from config import bot
from stateMachine import *
from handllers.mainMenu import number_request
from adminUser import admin_chat
import db
from buttone.menuKB import menu_kb
import json

router = Router()
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)

@router.message(StateFilter(UserReg.problem))
async def problem(message: types.Message, state: FSMContext):
    global all_user_data, global_phone_number

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    if str(message.text).lower() == 'назад':
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
    else:
        admin_data = db.get_admin_data()
        for i in admin_chat:
            await bot.send_message(i,
                                   "Новое обращение с вопросом!\nПользователь номер: {}\nНомер телефона: {}\nИмя: {}\nФамилия: {}\nВозраст: {}\nРегион: {}\nРазмер: {}\n".format(
                                       all_user_data[0], all_user_data[1], all_user_data[2], all_user_data[3],
                                       all_user_data[4], all_user_data[5], all_user_data[6]))
            try:
                if all_user_data[7][-3:] == 'pic':
                    await bot.send_photo(i, all_user_data[7][:-4], caption='Фото спереди:')
                else:
                    await bot.send_document(i, all_user_data[7][:-4], caption='Фото спереди:')
            except:
                await bot.send_message(i, 'Отсутствует фото спереди')
            try:
                if all_user_data[8][-3:] == 'pic':
                    await bot.send_photo(i, all_user_data[8][:-4], caption='Фото сзади:')
                else:
                    await bot.send_document(i, all_user_data[8][:-4], caption='Фото сзади:')
            except:
                await bot.send_message(i, 'Отсутствует фото сзади')

            try:
                if all_user_data[9][-3:] == 'pic':
                    await bot.send_photo(i, all_user_data[9][:-4], caption='Фото в профиль:')
                else:
                    await bot.send_document(i, all_user_data[9][:-4], caption='Фото в профиль:')
            except:
                await bot.send_message(i, 'Отсутствует фото в профиль')

            await bot.send_message(i, 'Текст проблемы:')
            await bot.forward_message(i, message.chat.id, message.message_id)
        kb = [
            [types.KeyboardButton(text="В меню")],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Менеджер свяжется с вами в течении 1 часа', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
