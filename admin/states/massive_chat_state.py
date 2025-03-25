from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_users

class MassiveChatState(StatesGroup):
    sending_massive_message = State()

router = Router()
@router.message(MassiveChatState.sending_massive_message)
async def send_massive_message(message: Message, state: FSMContext):
    text = message.text
    users = await get_users()
    for user in users:
        try:
            await message.bot.send_message(user["chat_id"], text)
        except Exception as e:
            print(f"Failed to send message to {user['chat_id']}: {e}")

    await message.answer("✅ Your message has been sent to all users.")
    await state.clear()