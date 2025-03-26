from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from config import FORM_REQUEST_GROUP_ID
from database import get_user
from keyboards.keyboards import main_menu, skip_step_2_keyboard, step_3_keyboard
from texts import second_step_text, third_step_text

class RequestFormSubmissionState(StatesGroup):
    address = State()
    media_image = State()
    subject = State()

router = Router()

@router.message(RequestFormSubmissionState.address)
async def handle_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(second_step_text, reply_markup=skip_step_2_keyboard(), parse_mode="HTML")
    await state.set_state(RequestFormSubmissionState.media_image)

@router.message(RequestFormSubmissionState.media_image, F.content_type.in_({ContentType.PHOTO, ContentType.TEXT}))
async def handle_media_image(message: Message, state: FSMContext):
    if message.photo:
        # Save the image file_id
        await state.update_data(media_image=message.photo[-1].file_id)
        await message.answer(third_step_text, reply_markup=step_3_keyboard(), parse_mode="HTML")
        await state.set_state(RequestFormSubmissionState.subject)
    elif message.text and message.text.lower() == "skip":
        # Allow skipping the image
        await state.update_data(media_image=None)
        text = "⛔️📛В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> в виде медиа-сообщения.\n<b>Попробуйте ещё раз:</b>"
        await message.answer(text, parse_mode="HTML")
        await state.set_state(RequestFormSubmissionState.subject)
    else:
        text = "⛔️📛В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> в виде медиа-сообщения.\n<b>Попробуйте ещё раз:</b>"
        await message.answer(text, parse_mode="HTML")

@router.message(RequestFormSubmissionState.subject)
async def handle_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    data = await state.get_data()

    address = data.get("address")
    media_image = data.get("media_image")
    subject = data.get("subject")
    user = await get_user(message.from_user.id)
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"

    admin_message = f"    ⛔️Поступила новая жалоба:\n\n" \
                    f"{username}\n" \
                    f"<b>Имя и Фамилия:</b> {user['full_name']}\n" \
                    f"<b>Номер телефона:</b> {user['phone_number']}\n" \
                    f"<b>Адрес</b>: {address}\n" \
                    f"<b>Содержание:</b> {subject}"
    if media_image:
        await message.bot.send_photo(FORM_REQUEST_GROUP_ID, media_image)

    await message.bot.send_message(FORM_REQUEST_GROUP_ID, admin_message, parse_mode="HTML")
    await state.clear()
    text = "✅<b>Жалоба отправлена администрации.</b> Спасибо за Ваше обращение!"
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())
