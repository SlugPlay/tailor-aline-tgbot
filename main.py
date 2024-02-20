import asyncio
import logging
import json
import db

from aiogram import Bot, Dispatcher, types, fsm, filters, F
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

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


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
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
    phone = str(message.text)
    data_users = await db.get_phone_status()
    flag1 = 'newUser'
    for i in range(len(data_users)):
        if phone == str(data_users[i][0]):
            flag1 = str(data_users[i][1])
            print(flag1)
    if flag1 == 'newUser':
        await message.answer('Введите свое имя')
        await state.set_state(UserState.newUser)
    elif flag1 == 'ageUser':
        print(1)
        await state.set_state(UserState.newUser)
    elif flag1 == 'admin':
        print(3)
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
    recInformation = str(message.text)
    user_info.append(recInformation)
    await message.answer('Введите свою фамилию')
    await state.set_state(UserReg.lastName)
    


@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    recInformation = str(message.text)
    user_info.append(recInformation)
    await message.answer('Введите свой возраст')
    await state.set_state(UserReg.age)


@dp.message(StateFilter(UserReg.age))
async def reg(message: types.Message, state: FSMContext):
    recInformation = str(message.text)
    user_info.append(recInformation)
    await message.answer('Выберите свой регион')
    await state.set_state(UserReg.region)


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
