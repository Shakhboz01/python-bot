from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import CALLBACK_REQUESTS_GROUP_ID
from database import close_tickets, get_user
from keyboards.keyboards import (
    ask_if_phone_number_is_correct,
    close_dialog_keyboard,
    main_menu,
    skip_step_1_keyboard,
    skip_step_2_keyboard,
    step_3_keyboard,
)
from aiogram.fsm.context import FSMContext
from states.account_settings_state import AccountSettingsState
from states.chat_with_admin_state import ChatWithAdminState
from states.suggestion_state import SuggestionState
from states.request_form_submission_state import RequestFormSubmissionState
from texts import first_step_text, second_step_text, third_step_text

router = Router()

@router.callback_query(F.data == "change_name")
async def change_name_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🛠️ Отправьте своё Имя и Фамилию, чтобы поменять настройки:")
    await callback.answer()
    await state.set_state(AccountSettingsState.full_name)

@router.callback_query(F.data == "change_number")
async def change_number_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🛠️ Отправьте свой номер телефона, чтобы поменять настройки:")
    await callback.answer()
    await state.set_state(AccountSettingsState.phone_number)

@router.callback_query(F.data == 'make_sugestion')
async def make_suggestion(callback: CallbackQuery, state: FSMContext):
    text = "<b>💡Распишите предложение в " \
           "подробностях: (Добавьте фотографию если есть)</b>"
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()
    await state.set_state(SuggestionState.suggestion)

@router.callback_query(F.data == 'request_form_submission')
async def request_form_submission(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(first_step_text, reply_markup=skip_step_1_keyboard(), parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.address)

@router.callback_query(F.data == 'skip_request_form_submission_step_1')
async def skip_request_form_submission_step_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(second_step_text, reply_markup=skip_step_2_keyboard(), parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.media_image)

@router.callback_query(F.data == 'skip_request_form_submission_step_2')
async def skip_request_form_submission_step_2(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(third_step_text, reply_markup=step_3_keyboard(), parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.subject)

@router.callback_query(F.data == "go_back_to_main")
async def go_back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "call_me")
async def call_me_callback(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    text = f"<b>Это Ваш верный номер телефона {user["phone_number"]}?</b> " \
           f"Если да, нажмите соответствующую кнопку, <b>если нет,</b> впишите свой актуальный номер телефона здесь"
    await callback.message.answer(text, reply_markup=ask_if_phone_number_is_correct(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "send_callback_request_notification")
async def send_callback_request_notification(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    text = "✅<b>Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время."
    await callback.message.answer(text, parse_mode="HTML", reply_markup=main_menu())
    await callback.answer()
    # Send notification to the admin
    await callback.message.bot.send_message(CALLBACK_REQUESTS_GROUP_ID, f"📞 Пользователь просит перезвонить ему. {user['phone_number']}")

@router.callback_query(F.data == "chat_bot")
async def chat_bot_callback(callback: CallbackQuery, state = FSMContext):
    text = "✅✅📞 Добрый день! Я - диспетчер управляющей компании 'УЭР-ЮГ', готов помочь Вам. Напишите, пожалуйста, интересующий Вас вопрос и ожидайте."
    await callback.message.answer(text=text, reply_markup=close_dialog_keyboard())
    await callback.answer()
    await state.set_state(ChatWithAdminState.message)

@router.callback_query(F.data == "close_dialog")
async def close_dialog_callback(callback: CallbackQuery, state= FSMContext):
    await callback.message.answer("❌📞<b>Диалог с администратором завершён...<b/>", parse_mode='HTML')
    await callback.answer()
    await state.clear()
    await close_tickets(callback.from_user.id)
