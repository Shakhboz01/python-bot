from aiogram import Router, F
from aiogram.types import Message

router = Router()
@router.message(F.text.lower() == "полезные контакты")
async def contacts_info_handler(message: Message):
    print(f"Received text: {message.text}")
    await message.answer("Hello! Here is a contacts")
