import asyncio
import logging
from aiogram import Bot, Dispatcher, types, fsm
from aiogram.fsm import state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext



bot = Bot(token="6984947559:AAHpR2pdf9oEOwJ2ReS7yp4QUb5gNk91rO8")
# Диспетчер
dp = Dispatcher()

flag = 0

class UserState(StatesGroup):
    name = State()
    addres = State()

@dp.message(StateFilter(None), Command('test'))
async def user_register(message: types.Message, state: FSMContext):
    await message.answer("Введите своё имя")
    if flag == 1:
        await state.set_state(UserState.name)
    else:
        await state.set_state(UserState.addres)
@dp.message(StateFilter(UserState.name))
async def user_register(message: types.Message, state: FSMContext):
    #await state.update_data(username=message.text)
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
