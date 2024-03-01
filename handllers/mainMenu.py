from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from adminUser import admin_users
from stateMachine import *
from handllers.menuStart import number_request
import db
from buttone.menuKB import menu_kb
from buttone.order_new import order_new
from buttone.order_old import order_old
import json

router = Router()


global_phone_number = number_request()
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)


@router.message(StateFilter(UserState.ageUser))
async def menu2(message: types.Message, state: FSMContext):
    await message.answer(str(f.get('order')), reply_markup=menu_kb)
    await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.menu))
async def menedq(message: types.Message, state: FSMContext):
    global global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    have_user_merki = 'no'
    if str(message.text) == f.get('menedger'):
        kb = [
            [types.KeyboardButton(text="Назад")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Напишите свою проблему, или нажмите кнопку 'Назад'", reply_markup=keyboard)
        await state.set_state(UserReg.problem)
    elif str(message.text) == f.get('skirt'):
        if all_user_data[-3]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            await message.answer("Давайте снимим с вас мерки", reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer("Выберите действие", reply_markup=order_old)
        await state.set_state(UserMenu.underSkirt)
    elif str(message.text) == f.get('throusres'):
        if all_user_data[-2]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':

            await message.answer("Давайте снимим с вас мерки", reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer("Выберите действие", reply_markup=order_old)
        await state.set_state(UserMenu.underTrousers)
    elif str(message.text) == f.get('top'):
        if all_user_data[-1]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':

            await message.answer("Давайте снимим с вас мерки", reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer("Выберите действие", reply_markup=order_old)
        await state.set_state(UserMenu.top)
    elif str(message.text) == f.get('perereg'):
        kb = [
            [types.KeyboardButton(text="Да")],
            [types.KeyboardButton(text="Нет")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Вы точно хотите пройти процесс регистрации заново?', reply_markup=keyboard)
        await state.set_state(UserMenu.registration_again)
    elif str(message.text).lower() == 'вернуться в панель админа' and global_phone_number in admin_users:
        kb = [
            [types.KeyboardButton(text="Получить список всех пользователей")],
            [types.KeyboardButton(text="Вывести все заявки")],
            [types.KeyboardButton(text="В меню")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Открываю панель управления...\nбип-буп-бип", reply_markup=keyboard)
        await state.set_state(UserState.admin)


@router.message(StateFilter(UserMenu.registration_again))
async def perereg(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'да':
        db.delete_user(global_phone_number)
        kb = [
            [types.KeyboardButton(text="Предоставить номер телефона", request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        nomer = await message.answer('Здравствуйте, предоставьте свой номер телефона', reply_markup=keyboard)
        await state.set_state(UserState.centr)
    else:
        await message.answer("Возвращаю вас в меню...")

        await message.answer("Что вы хотите заказать?", reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
