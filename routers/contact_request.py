from aiogram import Router, F
from aiogram.types import Message
from keyboards.keyboards import get_contact_keyboard as keyboard

router = Router()

@router.message(F.text.lower() == 'связаться')
async def contact_request(message: Message):
    text = ("🫵 Выберите способ связи из ниже перечисленного списка:")
    await message.answer(text, reply_markup=keyboard(), parse_mode="HTML")
