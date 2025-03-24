from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from keyboards.main_keyboard import main_menu
from aiogram.fsm.context import FSMContext
from states.account_settings_state import AccountSettingsState
from states.suggestion_state import SuggestionState
from states.request_form_submission_state import RequestFormSubmissionState

router = Router()
@router.callback_query(F.data == "change_name")
async def change_name_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✍️ Пожалуйста, отправьте мне ваше новое имя и фамилию.")
    await callback.answer()
    await state.set_state(AccountSettingsState.full_name)

@router.callback_query(F.data == "change_number")
async def change_number_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📱 Пожалуйста, отправьте ваш новый номер телефона.")
    await callback.answer()
    await state.set_state(AccountSettingsState.phone_number)

@router.callback_query(F.data == 'make_sugestion')
async def make_suggestion(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Распишите предложение в подробностях: (Добавьте фотографию если есть)")
    await callback.answer()
    await state.set_state(SuggestionState.suggestion)


@router.callback_query(F.data == 'request_form_submission')
async def request_form_submission(callback: CallbackQuery, state: FSMContext):
    text = "<b>Шаг 1/3.</b> Напишите адрес или ориентир проблемы"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_request_form_submission_step_1"),],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main"),],
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.address)


@router.callback_query(F.data == 'skip_request_form_submission_step_1')
async def request_form_submission(callback: CallbackQuery, state: FSMContext):
    text = "<b>Шаг 2/3.</b> Прикрепите фотографию проблемы"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_request_form_submission_step_2"),],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main"),],
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.media_image)

@router.callback_query(F.data == 'skip_request_form_submission_step_2')
async def request_form_submission(callback: CallbackQuery, state: FSMContext):
    text = "<b>Шаг 3/3.</b> Напишите причины обращения в подробностях"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
    await state.set_state(RequestFormSubmissionState.subject)


@router.callback_query(F.data == "go_back_to_main")
async def go_back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())
    await callback.answer()
    await state.clear()
