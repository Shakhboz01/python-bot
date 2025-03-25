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

# Inline keyboard for unsolved tickets
def unsolved_tickets_keyboard(tickets):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Ticket #{ticket['id']} (User: {ticket['user_id']})",
                    callback_data=f"ticket:{ticket['id']}"
                )
            ]
            for ticket in tickets
        ]
    )
    return keyboard

# Inline keyboard for ticket actions
def ticket_actions_keyboard(ticket_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Mark as Solved", callback_data=f"mark_solved:{ticket_id}"),
                InlineKeyboardButton(text="💬 Show Chats", callback_data=f"show_chats:{ticket_id}")
            ]
        ]
    )
    return keyboard

def user_list_keyboard(users, page):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for user in users:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{user['full_name']} ({'Banned' if user['is_banned'] else 'Active'})",
                callback_data=f"toggle_ban:{user['chat_id']}"
            )
        ])

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Previous", callback_data=f"page:{page - 1}"))
    pagination_buttons.append(InlineKeyboardButton(text="➡️ Next", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        keyboard.inline_keyboard.append(pagination_buttons)

    return keyboard
