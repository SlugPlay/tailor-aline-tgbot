import asyncio
import logging
import json

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


flag1 = 'newUser'


@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте, введите свой номер телефона')
    await state.set_state(UserState.centr)


@dp.message(StateFilter(UserState.centr))
async def user_start(message: types.Message, state: FSMContext):
    print(str(message.text), 'phone')
    if flag1 == 'newUser':
        await message.answer('Введите свое имя')
        await state.set_state(UserState.newUser)
    elif flag1 == 'ageUser':
        await state.set_state(UserState.ageUser)
    elif flag1 == 'admin':
        await state.set_state(UserState.admin)


@dp.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    print(str(message.text), 'firstname')
    await message.answer('Введите свою фамилию')
    await state.set_state(UserReg.lastName)

    recInformation = ''


@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    print(str(message.text), "lastname")
    await message.answer('Введите свой возраст')
    await state.set_state(UserReg.age)

    recInformation = ''


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



@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
files.close()