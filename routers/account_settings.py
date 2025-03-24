from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(F.text.lower() == "⚙️ настройки")
async def account_settings(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠️Поменять имя", callback_data="change_name"),
            InlineKeyboardButton(text="🛠️Сменить номер", callback_data="change_number")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back_to_main")
        ]
    ])

    text = (
        "⚙️ Тут Вы сможете поменять <b>Имя</b> и <b>Фамилию</b> в Базе данных нашего бота "
        "или же можете поменять Ваш <b>номер телефона</b>, если Вы изначально вводили что-то неверно. "
        "Выберите, что хотите поменять или вернитесь назад в <b>главное меню</b>:"
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
