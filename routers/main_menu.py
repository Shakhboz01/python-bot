from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from database import get_user
from keyboards.keyboards import main_menu
from states.registration_state import RegistrationState
from aiogram.fsm.context import FSMContext

main_router = Router()

# 🏠 Main Menu
@main_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    user = await get_user(chat_id)

    if user:
        await message.answer("Welcome back! 🎉", reply_markup=main_menu(is_admin = user['is_admin']))
    else:
        await message.answer("Hello! What's your full name?")
        await state.set_state(RegistrationState.full_name)
