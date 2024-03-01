import asyncio
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

# ---------------------------------------

dp = Dispatcher()

flag1 = ''

recInformation = ''

dp.message.middleware(SomeMiddleware())


async def main():
    dp.include_router(menuStart.router)
    dp.include_router(admin.router)
    dp.include_router(mainMenu.router)
    dp.include_router(menedger.router)
    dp.include_router(skirt.router)
    dp.include_router(trousers.router)
    dp.include_router(top.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
