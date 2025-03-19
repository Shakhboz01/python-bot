from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Оставить заявку'),
                KeyboardButton(text='Связаться')
            ],
            [KeyboardButton(text='⚙️ Настройки')],
            [KeyboardButton(text='Полезные контакты')],
        ],
        resize_keyboard=True
    )
    return keyboard
