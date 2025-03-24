from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import get_user

class SuggestionState(StatesGroup):
    suggestion = State()

router = Router()
@router.message(SuggestionState.suggestion)
async def process_suggestion(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("❌ Ваше предложение должно содержать текст. Отправьте текст или текст с изображением.")
        return

    suggestion_text = message.text
    user = await get_user(message.from_user.id)
    photo_id = message.photo[-1].file_id if message.photo else None

    admin_message = f"💡 *Поступило новое предложение:*\n\n" \
                    f"👤 Пользователь: {user['full_name']}\n" \
                    f"👤 Номер телефона: {user['phone_number']}\n" \
                    f"📝 Содержание: {suggestion_text}"

    await message.bot.send_message(-4631587118, admin_message, parse_mode="Markdown")

    if photo_id:
        await message.bot.send_photo(-4631587118, photo=photo_id)

    await message.answer("✅ Ваше предложение принято и отправлено на рассмотрение!")
    await state.clear()
