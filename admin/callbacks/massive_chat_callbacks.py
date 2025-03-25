from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin.states.massive_chat_state import MassiveChatState
from middlewares.admin_check import AdminCheckMiddleware

router = Router()
router.message.middleware(AdminCheckMiddleware())

@router.message(F.text.lower() == "массовая рассылка")
async def massive_chat(message: Message, state = FSMContext):
    await message.answer("Введите текст сообщения для массовой рассылки:")
    await state.set_state(MassiveChatState.sending_massive_message)
