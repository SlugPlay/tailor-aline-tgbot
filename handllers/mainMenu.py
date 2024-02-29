from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from tailor_aline_tgbot.adminUser import admin_users
from tailor_aline_tgbot.stateMachine import *
from tailor_aline_tgbot.globall import *
from tailor_aline_tgbot import db

router = Router()


@router.message(StateFilter(UserState.ageUser))
async def menu2(message: types.Message, state: FSMContext):
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


@router.message(StateFilter(UserMenu.menu))
async def menedq(message: types.Message, state: FSMContext):
    # что?
    # что?
    # что?
    # что?
    have_user_merki = 'no'
    # что?
    # что?
    # что?
    if str(message.text).lower() == 'связаться с менеджером':
        kb = [
            [types.KeyboardButton(text="Назад")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Напишите свою проблему, или нажмите кнопку 'Назад'", reply_markup=keyboard)
        await state.set_state(UserReg.problem)
    elif str(message.text).lower() == 'хочу заказать низ юбка':
        if all_user_data[-3]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underSkirt)
    elif str(message.text).lower() == 'хочу заказать низ брюки':
        if all_user_data[-2]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underTrousers)
    elif str(message.text).lower() == 'хочу заказать верх (платье, блузка, жакет, рубашка)':
        if all_user_data[-1]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
                [types.KeyboardButton(text="Назад")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.top)
    elif str(message.text).lower() == 'зарегистрироваться заново':
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
