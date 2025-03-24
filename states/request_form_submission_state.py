from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.fsm.context import FSMContext
from config import FORM_REQUEST_GROUP_ID
from database import get_user

class RequestFormSubmissionState(StatesGroup):
    address = State()
    media_image = State()
    subject = State()

router = Router()

@router.message(RequestFormSubmissionState.address)
async def handle_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    text = "<b>Шаг 2/3.</b> Фотография проблемы"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_request_form_submission_step_2")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main")],
        ]
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(RequestFormSubmissionState.media_image)

@router.message(RequestFormSubmissionState.media_image, F.content_type.in_({ContentType.PHOTO, ContentType.TEXT}))
async def handle_media_image(message: Message, state: FSMContext):
    if message.photo:
        # Save the image file_id
        await state.update_data(media_image=message.photo[-1].file_id)
        text = "<b>Шаг 3/3.</b> Напишите причины обращения в подробностях"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main")]
            ]
        )
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(RequestFormSubmissionState.subject)
    elif message.text and message.text.lower() == "skip":
        # Allow skipping the image
        await state.update_data(media_image=None)
        await message.answer("📩 No image provided. Now, please provide the subject.")
        await state.set_state(RequestFormSubmissionState.subject)
    else:
        await message.answer("❌ Please upload a valid image or type 'skip'.")

@router.message(RequestFormSubmissionState.subject)
async def handle_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    data = await state.get_data()

    address = data.get("address")
    media_image = data.get("media_image")
    subject = data.get("subject")
    user = await get_user(message.from_user.id)
    admin_message = f"💡 *Поступила новая жалоба:*\n\n" \
                f"👤 Пользователь: {user['full_name']}\n" \
                f"👤 Номер телефона: {user['phone_number']}\n" \
                f"Adress: {address}\n" \
                f"📝 Содержание: {subject}"

    await message.bot.send_message(FORM_REQUEST_GROUP_ID, admin_message, parse_mode="Markdown")

    if media_image:
        await message.bot.send_photo(FORM_REQUEST_GROUP_ID, media_image)

    await state.clear()
    await message.answer("✅ Your request submitted successfully")
