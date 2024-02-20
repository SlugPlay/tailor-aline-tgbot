import asyncio
import logging
import json
import re

from aiogram import Bot, Dispatcher, types, fsm
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

#Зависимости----------------------------------------------------------------------------------------------------------
file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
user_info = []

def check(text, type):
    if type == 'lang':
        regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
        pattern = re.compile(regex)
        return pattern.search(text) is not None
    if type == 'num':
        return text.isdigit()



# Диспетчер
dp = Dispatcher()


class UserState(StatesGroup):
    newUser = State()
    ageUser = State()
    admin = State()


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    clothingSize = State()


flag = 'newUser'


@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте, введите свою номер')
    if flag == 'newUser':
        await state.set_state(UserState.newUser)
    elif flag == 'ageUser':
        await state.set_state(UserState.ageUser)
    elif flag == 'admin':
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
    await state.set_state(UserReg.name)


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
