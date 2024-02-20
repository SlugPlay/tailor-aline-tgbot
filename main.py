import asyncio
import logging
import json
import db

from aiogram import Bot, Dispatcher, types, fsm, filters, F
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

files = open('dataset.txt', 'w')
# Зависимости----------------------------------------------------------------------------------------------------------
file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
user_info = []
flag1 = ''


# Диспетчер
dp = Dispatcher()
recInformation = ''


class UserState(StatesGroup):
    centr = State()
    newUser = State()
    admin = State()

mes = [0]
class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    regionAnother = State()
    clothingSize = State()

class CoolerUser(StatesGroup):
    ageUser = State()


@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await db.create_db()
    await message.answer('Здравствуйте, введите свой номер телефона')
    await state.set_state(UserState.centr)


@dp.message(StateFilter(UserState.centr))
async def user_start(message: types.Message, state: FSMContext):
<<<<<<< main.py
    phone = str(message.text)
    data_users = await db.get_phone_status()
    flag1 = 'newUser'
    for i in range(len(data_users)):
        if phone == str(data_users[i][0]):
            flag1 = str(data_users[i][1])
            print(flag1)
    print(str(message.text), 'phone')
    if flag1 == 'newUser':
        await message.answer('Введите свое имя')
        await state.set_state(UserState.newUser)
    elif flag1 == 'ageUser':
        print(1)
        await state.set_state(UserState.newUser)
    elif flag1 == 'admin':
        print(3)
        await state.set_state(UserState.admin)


@dp.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    recInformation = str(message.text)
    user_info.append(recInformation)
    await message.answer('Введите свою фамилию')
    await state.set_state(UserReg.lastName)
    print(str(message.text), 'firstname')


@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    recInformation = str(message.text)
    user_info.append(recInformation)
    await message.answer('Введите свой возраст')
    await state.set_state(UserReg.age)
    print(str(message.text), "lastname")


@dp.message(StateFilter(UserReg.age))
async def regRegio(message: types.Message, state: FSMContext):
    recInformation = message.text
    print(str(recInformation), 'age')
    kb = [
        [types.KeyboardButton(text="Санкт-Петербург"), types.KeyboardButton(text="Москва")],
        [types.KeyboardButton(text="Другой")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите свой регион из доступных", reply_markup=keyboard)
    await state.set_state(UserReg.regionAnother)


@dp.message(StateFilter(UserReg.regionAnother))
async def reg(message: types.Message, state: FSMContext):
    recInformation = str(message.text)
    user_info.append(recInformation)
    if str(message.text).lower() == 'другой':
        await message.answer('Введите свой регион')
        await state.set_state(UserReg.regionAnother)
    else:
        print(str(message.text), 'region')
        kb = [
            [types.KeyboardButton(text="XXS"), types.KeyboardButton(text="XS"),
             types.KeyboardButton(text="S"), types.KeyboardButton(text="M")],
            [types.KeyboardButton(text="L"), types.KeyboardButton(text="XL"),
             types.KeyboardButton(text="XXL"), types.KeyboardButton(text="XXXL")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите свой размер", reply_markup=keyboard)
        await state.set_state(UserReg.regionAnother)
        print(str(message.text), 'size')

    recInformation = ''


# @dp.message(Command('photo'))
# async def echo_photo_message(message: types.Message, state: FSMContext, bot: Bot):
#     await message.answer('пришлите фото')
#     file = await bot.get_file(message.document.file_id)
#     await message.photo(file)

@dp.message(StateFilter(CoolerUser.ageUser))
async def menu(message: types.Message, state: FSMContext):
    print(2)
    await message.answer('Олух')


@dp.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    print(4)
    await message.answer('Тварь')


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
files.close()