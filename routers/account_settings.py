from aiogram import Router, F
from aiogram.types import Message
from keyboards.keyboards import account_settings_keyboard
router = Router()

@router.message(F.text.lower() == "⚙️ настройки")
async def account_settings(message: Message):
    text = (
        "⚙️ Тут Вы сможете поменять <b>Имя</b> и <b>Фамилию</b> в Базе данных нашего бота "
        "или же можете поменять Ваш <b>номер телефона</b>, если Вы изначально вводили что-то неверно. "
        "Выберите, что хотите поменять или вернитесь назад в <b>главное меню</b>:"
    )

    await message.answer(text, reply_markup=account_settings_keyboard(), parse_mode="HTML")
