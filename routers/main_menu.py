from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from database import get_user
from keyboards.keyboards import main_menu
from states.registration_state import RegistrationState
from aiogram.fsm.context import FSMContext
from states.registration_state import welcome_message_text

main_router = Router()

# 🏠 Main Menu
@main_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    user = await get_user(chat_id)

    if user:
        await message.answer(welcome_message_text, parse_mode="HTML", reply_markup=main_menu(is_admin=user['is_admin']), passe_mode="HTML")
    else:
        text = "🌞 <b>Доброго времени суток,</b> бот создан, чтобы обрабатывать заявки и " \
               "обращения пользователей. Чтобы воспользоваться этим, пришлите для начала Ваше <b>Имя</b> и <b>Фамилию</b>"
        await message.answer(text, parse_mode="HTML")
        await state.set_state(RegistrationState.full_name)
