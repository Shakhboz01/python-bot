from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main_keyboard import main_menu

router = Router()

@router.callback_query(F.data == "change_name")
async def change_name_callback(callback: CallbackQuery):
    await callback.message.answer("✍️ Пожалуйста, отправьте мне ваше новое имя и фамилию.")
    await callback.answer()

@router.callback_query(F.data == "change_number")
async def change_number_callback(callback: CallbackQuery):
    await callback.message.answer("📱 Пожалуйста, отправьте ваш новый номер телефона.")
    await callback.answer()

@router.callback_query(F.data == "go_back_to_main")
async def go_back_callback(callback: CallbackQuery):
    await callback.message.answer("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())
    await callback.answer()
