import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types, fsm
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


#Зависимости----------------------------------------------------------------------------------------------------------
file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))

# Диспетчер
dp = Dispatcher()


class UserState(StatesGroup):
    newUser = State()
    ageUser = State()
    admin = State()
    name = State()
    addres = State()


flag = 'newUse'


@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте, введите свой номер телефона')
    asyncio.run(central(flag))


async def central(flag, state: FSMContext):
    if flag == 'newUser':
        asyncio.run(user_register())
    else:
        asyncio.run(test())


@dp.message(StateFilter(None))
async def test(message: types.Message):
    await message.answer("Введите qweq")


@dp.message(StateFilter(None))
async def user_register(message: types.Message, state: FSMContext):
    await message.answer("Введите своё имя")
    await state.set_state(UserState.name)


@dp.message(StateFilter(UserState.name))
async def user_register(message: types.Message, state: FSMContext):
    await message.answer("Введите свою фамилию")
    await state.set_state(UserState.addres)


@dp.message(StateFilter(UserState.addres))
async def user_reg(message: types.Message, state: FSMContext):
    await message.reply('Иди нахуй')
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
