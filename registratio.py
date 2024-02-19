from main import bot, dp

import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, fsm
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


async def gl_reg(idi):
    async def start_reg():
        await bot.send_message(chat_id=idi, text='Введите ваш возраст')
    
    @dp.message()
    async def second_reg(message: types.Message):
        text = message.text
        await message.answer(text=text)
    
    await start_reg()