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
    name = State()
    addres = State()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
