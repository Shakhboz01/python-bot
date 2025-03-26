from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import get_user
from config import SUGGESTION_GROUP_ID
class SuggestionState(StatesGroup):
    suggestion = State()

router = Router()

@router.message(SuggestionState.suggestion)
async def process_suggestion(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("⛔📛Предложение должно содержать только текст.")
        return

    suggestion_text = message.text
    user = await get_user(message.from_user.id)
    photo_id = message.photo[-1].file_id if message.photo else None

    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"

    admin_message = (
        "     💡Поступило новое предложение:\n\n"
        f"{username}\n"
        f"<b>Имя и Фамилия:</b> {user['full_name']}\n"
        f"<b>Номер телефона:</b> {user['phone_number']}\n"
        f"<b>Содержание:</b> {suggestion_text}"
    )

    await message.bot.send_message(SUGGESTION_GROUP_ID, admin_message, parse_mode="HTML")

    if photo_id:
        await message.bot.send_photo(SUGGESTION_GROUP_ID, photo=photo_id)

    await message.answer("✅💡<b>Идея принята и передана администрации.</b> Спасибо за Ваше обращение!", parse_mode="HTML")
    await state.clear()
