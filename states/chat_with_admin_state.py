from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import create_incoming_chat

class ChatWithAdminState(StatesGroup):
    message = State()

router = Router()
@router.message(ChatWithAdminState.message)
async def process_chat_with_admin(message: Message):
    if not message.text:
        await message.answer("❌")
        return

    message_text = message.text
    await create_incoming_chat(message.from_user.id, message_text)
