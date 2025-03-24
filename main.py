import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import create_table
from middlewares.banned_user import BanCheckMiddleware
from handlers.callbacks import router as callback_router

from routers.main_menu import main_router
from routers.account_settings import router as account_settings_router
from routers.contacts_info import router as contacts_info_router

from states.registration_state import router as registration_state_router
from states.account_settings_state import router as account_settings_state_router


async def main():
    logging.basicConfig(level=logging.INFO)

    await create_table()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.message.middleware(BanCheckMiddleware())
    dp.include_router(account_settings_router)
    dp.include_router(registration_state_router)
    dp.include_router(account_settings_state_router)
    dp.include_router(contacts_info_router)
    dp.include_router(callback_router)
    dp.include_router(main_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
