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
from routers.request_submission import router as request_submission_router
from routers.contact_request import router as contact_request_router
from states.registration_state import router as registration_state_router
from states.account_settings_state import router as account_settings_state_router
from states.suggestion_state import router as suggestion_state_router
from states.request_form_submission_state import router as request_form_submission_router
from states.chat_with_admin_state import router as chat_with_admin_router
from admin.callbacks import router as admin_callbacks_router
from admin.users import router as admin_users_router

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
    dp.include_router(request_submission_router)
    dp.include_router(suggestion_state_router)
    dp.include_router(request_form_submission_router)
    dp.include_router(contact_request_router)
    dp.include_router(chat_with_admin_router)
    dp.include_router(main_router)
    dp.include_router(admin_users_router)
    dp.include_router(admin_callbacks_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
