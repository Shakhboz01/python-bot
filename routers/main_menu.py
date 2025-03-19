from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from database import get_user, add_user, CYRILLIC_NAME_REGEX, PHONE_REGEX
from keyboards.main_keyboard import main_menu
main_router = Router()
user_data = {}

# 🏠 Main Menu
@main_router.message(CommandStart())
async def start_handler(message: Message):
    chat_id = message.from_user.id
    user = await get_user(chat_id)

    if user:
        await message.answer("Welcome back! 🎉", reply_markup=main_menu())
    else:
        user_data[chat_id] = {}
        await message.answer("Hello! What's your full name?")

@main_router.message(F.text)
async def ask_full_name(message: Message):
    chat_id = message.from_user.id

    if chat_id in user_data and "full_name" not in user_data[chat_id]:
        if not CYRILLIC_NAME_REGEX.match(message.text):
            await message.answer('name mismatch')
            return

        user_data[chat_id]["full_name"] = message.text
        await message.answer("Great! share your phone number.")
    elif chat_id in user_data and "full_name" in user_data[chat_id]:
        print(f"User input is{message.text}")
        print(f"REGEX IS {PHONE_REGEX}")
        if not PHONE_REGEX.match(message.text.strip()):
            await message.answer('Phone number mismatch')
            return
        await add_user(chat_id, user_data[chat_id]["full_name"], message.text)
        del user_data[chat_id]
        await message.answer("✅ Registration completed!", reply_markup=main_menu())
