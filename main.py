import asyncio
import logging
import json
import db
from aiogram import Bot, Dispatcher, types, fsm, filters, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
# --------------------------------------------- photo-------------------------------------------
photo_1 = FSInputFile("photo_bot/Высота бедер.jpg")
photo_2 = FSInputFile("photo_bot/Высота груди.jpg")
photo_3 = FSInputFile("photo_bot/Высота переда до талии.jpg")
photo_4 = FSInputFile("photo_bot/Высота сиденья.jpg")
photo_5 = FSInputFile("photo_bot/Длина изделия (низ)(1).jpg")
photo_6 = FSInputFile("photo_bot/Длина изделия (низ).jpg")
photo_7 = FSInputFile("photo_bot/Длина изделия_.jpg")
photo_8 = FSInputFile("photo_bot/Длина спины до талии.jpg")
photo_9 = FSInputFile("photo_bot/Обхват бедер.jpg")
photo_10 = FSInputFile("photo_bot/Обхват груди 1.jpg")
photo_11 = FSInputFile("photo_bot/Ширина спины.jpg")
photo_12 = FSInputFile("photo_bot/Обхват груди 2.jpg")
photo_13 = FSInputFile("photo_bot/Обхват груди 3.jpg")
photo_14 = FSInputFile("photo_bot/Обхват запястья.jpg")
photo_15 = FSInputFile("photo_bot/Обхват плеча.jpg")
photo_16 = FSInputFile("photo_bot/Обхват талии.jpg")
photo_17 = FSInputFile("photo_bot/Обхват шеи.jpg")
photo_18 = FSInputFile("photo_bot/Центр груди.jpg")
photo_19 = FSInputFile("photo_bot/Ширина плеча_.jpg")
# --------------------------------------------- photo-------------------------------------------
flag1 = ''

# Диспетчер
dp = Dispatcher()
recInformation = ''


class UserState(StatesGroup):
    centr = State()
    newUser = State()
    ageUser = State()
    admin = State()


mes = [0]


class UserSize(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()
    step6 = State()
    step7 = State()
    step8 = State()
    step9 = State()
    step10 = State()
    step11 = State()
    step12 = State()
    step13 = State()
    step14 = State()
    step15 = State()
    step16 = State()
    step17 = State()
    step18 = State()
    step19 = State()
    step20 = State()
    step21 = State()
    step22 = State()
    step23 = State()
    step24 = State()
    step25 = State()
    step26 = State()
    step27 = State()
    step28 = State()
    step29 = State()
    step30 = State()


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    regionAnother = State()
    clothingSize = State()
    photoFront = State()
    photoBack = State()
    photoProfile = State()


class UserMenu(StatesGroup):
    menu = State()
    meneg = State()
    underSkirt = State()
    underTrousers = State()
    top = State()
    orderTopVse = State()
    orderSkirt = State()
    orderTrousers = State()
    orderUnderTrousers = State()
    orderUnderSkirt = State()
    orderTop = State()


# --------------------------------------------- регистрация -------------------------------------------
@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await db.create_db()
    await message.answer('Здравствуйте, введите свой номер телефона')
    await state.set_state(UserState.centr)


@dp.message(StateFilter(UserState.centr))
async def user_start(message: types.Message, state: FSMContext):
    global user_info

    user_info = []
    phone = str(message.text)
    data_users = await db.get_phone_status()
    flag1 = 'newUser'
    for i in range(len(data_users)):
        if phone == str(data_users[i][0]):
            flag1 = str(data_users[i][1])
    if flag1 == 'newUser':
        user_info.append(int(message.chat.id))
        user_info.append(phone)
        await db.create_profile(user_info[0], user_info[1], 'newUser')
        user_info.append('ageUser')
        await message.answer('Введите свое имя')
        await state.set_state(UserState.newUser)
    elif flag1 == 'ageUser':
        await state.set_state(UserState.ageUser)
        kb = [
            [types.KeyboardButton(text="В меню")],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Привет имя пользователя', reply_markup=keyboard)
    elif flag1 == 'admin':
        await state.set_state(UserState.admin)


@dp.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    await message.answer('Введите свою фамилию')
    await state.set_state(UserReg.lastName)


@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    await message.answer('Введите свой возраст')
    await state.set_state(UserReg.age)


@dp.message(StateFilter(UserReg.age))
async def regRegio(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    kb = [
        [types.KeyboardButton(text="Санкт-Петербург"), types.KeyboardButton(text="Москва")],
        [types.KeyboardButton(text="Другой")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите свой регион из доступных", reply_markup=keyboard)
    await state.set_state(UserReg.regionAnother)


@dp.message(StateFilter(UserReg.regionAnother))
async def reg(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'другой':
        await message.answer('Введите свой регион', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserReg.regionAnother)
    else:
        user_info.append(str(message.text))
        kb = [
            [types.KeyboardButton(text="XXS"), types.KeyboardButton(text="XS"),
             types.KeyboardButton(text="S"), types.KeyboardButton(text="M")],
            [types.KeyboardButton(text="L"), types.KeyboardButton(text="XL"),
             types.KeyboardButton(text="XXL"), types.KeyboardButton(text="XXXL")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите свой размер", reply_markup=keyboard)
        await state.set_state(UserReg.clothingSize)


@dp.message(StateFilter(UserReg.clothingSize))
async def reg(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    await message.answer('Загрузите фото в полный рост спереди', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserReg.photoFront)


@dp.message(StateFilter(UserReg.photoFront))
async def reg(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_info.append(file_id)
    await message.answer('Загрузите фото в полный рост сзади')
    await state.set_state(UserReg.photoBack)


@dp.message(StateFilter(UserReg.photoBack))
async def reg(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_info.append(file_id)
    await message.answer('Загрузите фото в полный рост в профиль')
    await state.set_state(UserReg.photoProfile)


@dp.message(StateFilter(UserReg.photoProfile))
async def reg(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_info.append(file_id)
    user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile = user_info
    await db.edit_profile(user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back,
                          photo_profile)
    kb = [
        [types.KeyboardButton(text="В меню")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Привет имя пользователя', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- регистрация ------------------------------------
# --------------------------------------------- меню -------------------------------------------
@dp.message(StateFilter(UserState.ageUser))
async def menu(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
        [types.KeyboardButton(text="Хочу заказать низ Юбка")],
        [types.KeyboardButton(text="Хочу заказать низ Брюки")],
        [types.KeyboardButton(text="Связаться с менеджером")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Что вы хотите заказать", reply_markup=keyboard)
    await state.set_state(UserMenu.menu)


@dp.message(StateFilter(UserMenu.menu))
async def menedq(message: types.Message, state: FSMContext):
    flag1 = 'ageUser'  # проверка в базе данных!!!
    if str(message.text).lower() == 'связаться с менеджером':
        await message.answer('Введите текст проблемы, и с вами свяжется менеджер',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.meneg)
    elif str(message.text).lower() == 'хочу заказать низ юбка':
        if flag1 == 'newUser':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif flag1 == 'ageUser':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underSkirt)
    elif str(message.text).lower() == 'хочу заказать низ брюки':
        if flag1 == 'newUser':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif flag1 == 'ageUser':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underTrousers)
    elif str(message.text).lower() == 'хочу заказать верх (платье, блузка, жакет, рубашка)':
        if flag1 == 'newUser':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif flag1 == 'ageUser':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.top)


# --------------------------------------------- меню -------------------------------------------
# --------------------------------------------- менеджер ---------------------------------------
@dp.message(StateFilter(UserMenu.meneg))
async def problem(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Менеджер свяжется с вами в течении 1 часа', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- менеджер ---------------------------------------
# --------------------------------------------- низ юбка --------------------------------------------
@dp.message(StateFilter(UserMenu.underSkirt))
async def under(message: types.Message, state: FSMContext):
    print(str(message.text))
    if str(message.text).lower() == 'использовать старые мерки':
        print('максим')  # подгружаем базу данных
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text).lower() == 'сделаем мерки':
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderUnderSkirt)


@dp.message(StateFilter(UserMenu.orderUnderSkirt))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step1)


@dp.message(StateFilter(UserSize.step1))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_9, 'Обхват бедер')
    await state.set_state(UserSize.step2)


@dp.message(StateFilter(UserSize.step2))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_1, 'Высота бедер')
    await state.set_state(UserSize.step3)


@dp.message(StateFilter(UserSize.step3))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_7, 'Длина изделия')
    await state.set_state(UserSize.step4)


@dp.message(StateFilter(UserSize.step4))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderSkirt))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- низ юбка --------------------------------------------
# --------------------------------------------- низ брюки --------------------------------------------
@dp.message(StateFilter(UserMenu.underTrousers))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'использовать старые мерки':
        print('максим')  # подгружаем базу данных
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text).lower() == 'сделаем мерки':
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderUnderTrousers)


@dp.message(StateFilter(UserMenu.orderUnderTrousers))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step23)


@dp.message(StateFilter(UserSize.step23))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_9, 'Обхват бедер')
    await state.set_state(UserSize.step24)


@dp.message(StateFilter(UserSize.step24))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_1, 'Высота бедер')
    await state.set_state(UserSize.step25)


@dp.message(StateFilter(UserSize.step25))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_4, 'Высота сиденья')
    await state.set_state(UserSize.step26)


@dp.message(StateFilter(UserSize.step26))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_6, 'Длина брюк по боку')
    await state.set_state(UserSize.step27)


@dp.message(StateFilter(UserSize.step27))
async def under(message: types.Message, state: FSMContext):
    await message.answer('Загрузите одно-два фото желаемого изделия')
    # получаем фото
    await state.set_state(UserSize.step28)


@dp.message(StateFilter(UserSize.step28))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderTrousers))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- низ брюки --------------------------------------------
# --------------------------------------------- верх -------------------------------------------
@dp.message(StateFilter(UserMenu.top))
async def under(message: types.Message, state: FSMContext):
    print(str(message.text))
    if str(message.text).lower() == 'использовать старые мерки':
        print('максим')  # подгружаем базу данных
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTop)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTop)
    elif str(message.text).lower() == 'сделаем мерки':
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderTopVse)


@dp.message(StateFilter(UserMenu.orderTopVse))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_17, 'Обхват шеи', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step5)


@dp.message(StateFilter(UserSize.step5))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_10, 'Обхват груди 1')
    await state.set_state(UserSize.step6)


@dp.message(StateFilter(UserSize.step6))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_12, 'Обхват груди 2')
    await state.set_state(UserSize.step7)


@dp.message(StateFilter(UserSize.step7))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_13, 'Обхват груди 3')
    await state.set_state(UserSize.step8)


@dp.message(StateFilter(UserSize.step8))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_18, 'Центр груди')
    await state.set_state(UserSize.step9)


@dp.message(StateFilter(UserSize.step9))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_2, 'Высота груди')
    await state.set_state(UserSize.step10)


@dp.message(StateFilter(UserSize.step10))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_19, 'Ширина плеча')
    await state.set_state(UserSize.step11)


@dp.message(StateFilter(UserSize.step11))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_15, 'Обхват плеча')
    await state.set_state(UserSize.step12)


@dp.message(StateFilter(UserSize.step12))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_14, 'Обхват запястья')
    await state.set_state(UserSize.step13)


# нет фото!!!!! длина рукова
@dp.message(StateFilter(UserSize.step13))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_14, 'Длина рукава')
    await state.set_state(UserSize.step14)


@dp.message(StateFilter(UserSize.step14))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_16, 'Обхват талии')
    await state.set_state(UserSize.step15)


@dp.message(StateFilter(UserSize.step15))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_9, 'Обхват бедер')
    await state.set_state(UserSize.step16)


@dp.message(StateFilter(UserSize.step16))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_1, 'Высота бедер')
    await state.set_state(UserSize.step17)


@dp.message(StateFilter(UserSize.step17))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_11, 'Ширина спины')
    await state.set_state(UserSize.step18)


@dp.message(StateFilter(UserSize.step18))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_8, 'Длина спины до талии')
    await state.set_state(UserSize.step19)


@dp.message(StateFilter(UserSize.step19))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_8, 'Длина переда до талии')
    await state.set_state(UserSize.step20)


@dp.message(StateFilter(UserSize.step20))
async def under(message: types.Message, state: FSMContext):
    await message.answer_photo(photo_8, 'Длина изделия')
    await state.set_state(UserSize.step21)


@dp.message(StateFilter(UserSize.step21))
async def under(message: types.Message, state: FSMContext):
    await message.answer('Загрузите одно-два фото желаемого изделия')
    # получаем фото
    await state.set_state(UserSize.step22)


@dp.message(StateFilter(UserSize.step22))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderTop))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- верх -------------------------------------------


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
