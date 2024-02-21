import asyncio
import logging
import json
import db
from aiogram import Bot, Dispatcher, types, fsm, filters, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
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
    under = State()
    top = State()
    order = State()
    orderUnder = State()
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
        [types.KeyboardButton(text="Хочу заказать низ (Юбка, Брюки)")],
        [types.KeyboardButton(text="Связаться с менеджером")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Что хотите", reply_markup=keyboard)
    await state.set_state(UserMenu.menu)


@dp.message(StateFilter(UserMenu.menu))
async def mened(message: types.Message, state: FSMContext):
    flag1 = 'ageUser'  # проверка в базе данных!!!
    if str(message.text).lower() == 'связаться с менеджером':
        await message.answer('Введите текст проблемы, и с вами свяжется менеджер',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.meneg)
    elif str(message.text).lower() == 'хочу заказать низ (юбка, брюки)':
        if flag1 == 'newUser':
            kb = [
                [types.KeyboardButton(text="Начнем измерения")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif flag1 == 'ageUser':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)

        await state.set_state(UserMenu.under)
    elif str(message.text).lower() == 'хочу заказать верх (платье, блузка, жакет, рубашка)':
        if flag1 == 'newUser':
            kb = [
                [types.KeyboardButton(text="Начать измерения")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif flag1 == 'ageUser':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
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
# --------------------------------------------- низ --------------------------------------------
@dp.message(StateFilter(UserMenu.under))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'использовать старые мерки':
        print('максим')
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.order)
    elif str(message.text).lower() == 'cделаем мерки':
        print('Максим)))')
        await state.set_state(UserMenu.orderUnder)


@dp.message(StateFilter(UserMenu.order))
async def under(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- низ --------------------------------------------
# --------------------------------------------- верх -------------------------------------------
@dp.message(StateFilter(UserMenu.top))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'использовать старые мерки':
        print('максим')
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.order)
    elif str(message.text).lower() == 'cделаем мерки':
        print('Максим)))')
        await state.set_state(UserMenu.orderTop)


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
