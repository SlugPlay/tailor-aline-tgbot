import asyncio
import logging
from aiogram import Bot, Dispatcher, types, fsm
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

bot = Bot(token="6984947559:AAHpR2pdf9oEOwJ2ReS7yp4QUb5gNk91rO8")
# Диспетчер
dp = Dispatcher()


class UserState(StatesGroup):
    name = State()
    addres = State()

@dp.message(StateFilter(None), Command('test'))
async def user_register(message: types.Message):
    await message.answer("Введите своё имя")


@dp.message(StateFilter(UserState.name))
async def user_register(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите свою фамилию")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
