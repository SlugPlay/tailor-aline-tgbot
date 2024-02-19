
import asyncio
import logging
import json
import db
from aiogram import Bot, Dispatcher, types, fsm
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext



file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
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
    await message.answer('Здравствуйте, введите свой номер телефона')
    await db.create_db()

@dp.message()
async def user_start2(message: types.Message):
    text = str(message.text)

    idi = message.chat.id
    await central(text, idi)

async def central(type, idi):
    if type == 'newUser':
        await registration(idi)

async def registration(idi):
    async def start_reg():
        await bot.send_message(chat_id=idi, text='Введите ваш возраст')
        dp.message_reaction
        await bot.send_message(chat_id=idi, text='123 ваш возраст')
    
    @dp.message()
    async def second_reg(message: types.Message):
        text = str(message.text)
        await message.answer(text=text)
    
    await start_reg()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main()) 