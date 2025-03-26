from aiogram import Router, F
from aiogram.types import Message
from keyboards.keyboards import request_form_submission_keyboard as keyboard

router = Router()

@router.message(F.text.lower() == '📛 оставить заявку')
async def request_submission(message: Message):
    text = ("📛👇📛Выберите категорию, по которой Вы хотите оставить заявку в УК:")
    await message.answer(text, reply_markup=keyboard(), parse_mode="HTML")
