import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import create_table
from handlers import main_router

async def main():
    logging.basicConfig(level=logging.INFO)

    await create_table()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
