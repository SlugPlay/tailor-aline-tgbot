import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6984947559:AAHpR2pdf9oEOwJ2ReS7yp4QUb5gNk91rO8")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message()
async def cmd_start(message: types.Message):
    await message.answer("Введите свой номер")

@dp.message()
async def cmd_start1(message: types.Message):
    await message.answer("Введите свое имя")

@dp.message()
async def cmd_start2(message: types.Message):
    await message.answer("Введите свою фамилию")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)
    dp.message.register(cmd_start2)


if __name__ == "__main__":
    asyncio.run(main())