import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types, fsm, filters, F
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

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


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    clothingSize = State()


flag1 = 'newUser'


@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте, введите свой номер телефона')
    await state.set_state(UserState.centr)


@dp.message(StateFilter(UserState.centr))
async def user_start(message: types.Message, state: FSMContext):
    flag1 = str(message.text)
    # db_func(flag1)
    if flag1 == 'newUser':
        await message.answer('Введите свое имя')
        await state.set_state(UserState.newUser)
    elif flag1 == 'ageUser':
        await state.set_state(UserState.ageUser)
    elif flag1 == 'admin':
        await state.set_state(UserState.admin)


# async def central(flag, message):
#     if flag == 'newUser':
#         await reg()
#     elif flag == 'ageUser':
#         asyncio.run()
#     elif flag == 'admin':
#         asyncio.run()


@dp.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Введите свою фамилию')
    await state.set_state(UserReg.lastName)
    recInformation = ''


@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Введите свой возраст')
    await state.set_state(UserReg.age)
    recInformation = ''


@dp.message(StateFilter(UserReg.age))
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Выберите свой регион')
    await state.set_state(UserReg.region)
    recInformation = ''


# @dp.message(Command('photo'))
# async def echo_photo_message(message: types.Message, state: FSMContext, bot: Bot):
#     await message.answer('пришлите фото')
#     file = await bot.get_file(message.document.file_id)
#     await message.photo(file)


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
