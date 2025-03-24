from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(F.text.lower() == 'связаться')
async def account_settings(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оставить заявку", callback_data="request_form_submission"),
                InlineKeyboardButton(text="Поделиться предложением", callback_data="make_sugestion"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main"),
            ],
        ]
    )

    text = (
        "Выберите категорию, по которой вы хотите оставить заявку в УК:"
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
