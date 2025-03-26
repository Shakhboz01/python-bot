from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(is_admin=False):
    if is_admin:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Блокировать&Разблокировать пользователей')],
                [KeyboardButton(text='Нерешенные тикеты')],
                [KeyboardButton(text='Массовая рассылка')],
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📛 Оставить заявку'), KeyboardButton(text='📞Связаться')],
                [KeyboardButton(text='⚙️ Настройки')],
                [KeyboardButton(text='☎️ Полезные контакты')],
            ],
            resize_keyboard=True
        )
    return keyboard

def get_contact_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞Перезвоните мне", callback_data="call_me")],
        [InlineKeyboardButton(text="📞Свяжитесь со мной в чат-боте", callback_data="chat_bot")],
        [InlineKeyboardButton(text="🔙Назад", callback_data="go_back")]
    ])
    return keyboard

def account_settings_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠️ Поменять имя", callback_data="change_name"),
            InlineKeyboardButton(text="🛠️ Сменить номер", callback_data="change_number")
        ],

        [InlineKeyboardButton(text="🔙Назад", callback_data="go_back")]
    ])
    return keyboard

def request_form_submission_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📛Оставить заявку", callback_data="request_form_submission"),
                InlineKeyboardButton(text="💡Поделиться предложением", callback_data="make_sugestion"),
            ],
            [InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main"),],
        ]
    )
    return keyboard

def skip_step_1_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️Пропустить", callback_data="skip_request_form_submission_step_1")],
            [InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main")],
        ]
    )
    return keyboard

def skip_step_2_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️Пропустить", callback_data="skip_request_form_submission_step_2")],
            [InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main")],
        ]
    )
    return keyboard

def step_3_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main")]
        ]
    )
    return keyboard

def ask_if_phone_number_is_correct():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅Да", callback_data="send_callback_request_notification")],
            [InlineKeyboardButton(text="🔙Оставить номер телефона", callback_data="go_back_to_main")]
        ]
    )
    return keyboard

def close_dialog_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌📞Завершить диалог", callback_data="close_dialog")]
        ]
    )
    return keyboard
