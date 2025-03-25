from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def user_list_keyboard(users, page):
    keyboard = InlineKeyboardMarkup()
    for user in users:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{user['full_name']} ({'Banned' if user['is_banned'] else 'Active'})",
                callback_data=f"toggle_ban:{user['chat_id']}"
            )
        )
    # Add pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Previous", callback_data=f"page:{page - 1}"))
    pagination_buttons.append(InlineKeyboardButton(text="➡️ Next", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        keyboard.add(*pagination_buttons)

    return keyboard
