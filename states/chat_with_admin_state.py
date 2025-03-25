from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import create_incoming_chat, get_user
from keyboards.keyboards import close_dialog_keyboard

class ChatWithAdminState(StatesGroup):
    message = State()

router = Router()
@router.message(ChatWithAdminState.message)
# create a chat record in the database
async def process_chat_with_admin(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("❌ Your message should contain text. Send text or text with an image.")
        return

    message_text = message.text
    await create_incoming_chat(message.from_user.id, message_text)
    await message.answer("✅ Your message has been sent to the admin for review!", reply_markup=close_dialog_keyboard())
