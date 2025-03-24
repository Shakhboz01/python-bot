from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main_keyboard import main_menu
from aiogram.fsm.context import FSMContext
from states.account_settings_state import AccountSettingsState
from states.suggestion_state import SuggestionState
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

@router.callback_query(F.data == "go_back_to_main")
async def go_back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())
    await callback.answer()
    await state.clear()
