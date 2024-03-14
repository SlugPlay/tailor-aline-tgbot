import asyncio
import os

from aiogram import Dispatcher

# ----------------------------------------
from midleware import SomeMiddleware

# ---------------------------------------
import menuStart
import mainMenu
import admin
import menedger
import skirt
import trousers
import top
from config import *
import clothesMenu

# ---------------------------------------

dp = Dispatcher()

flag1 = ''

recInformation = ''

dp.message.middleware(SomeMiddleware())


async def main():
    os.system("pip freeze > requirements.txt")
    dp.include_router(menuStart.router)
    dp.include_router(admin.router)
    dp.include_router(mainMenu.router)
    dp.include_router(clothesMenu.router)
    dp.include_router(menedger.router)
    dp.include_router(skirt.router)
    dp.include_router(trousers.router)
    dp.include_router(top.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
