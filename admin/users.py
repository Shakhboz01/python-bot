from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import connect_db
from admin.keyboads import user_list_keyboard
from middlewares.admin_check import AdminCheckMiddleware

router = Router()
router.message.middleware(AdminCheckMiddleware())
USERS_PER_PAGE = 10

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

@router.message(F.text.lower() == "list users")
async def list_users(message: Message, state=None, page=1):
    db = await connect_db()
    offset = (page - 1) * USERS_PER_PAGE
    users = await db.fetch(
        "SELECT chat_id, full_name, is_banned FROM users ORDER BY chat_id LIMIT $1 OFFSET $2",
        USERS_PER_PAGE, offset
    )
    await db.close()

    if not users:
        await message.answer("❌ No users found.")
        return

    await message.answer("👥 List of users:", reply_markup=user_list_keyboard(users, page))

@router.callback_query(F.data.startswith("page:"))
async def paginate_users(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await list_users(callback.message, page=page)
    await callback.answer()

@router.callback_query(F.data.startswith("toggle_ban:"))
async def toggle_ban(callback: CallbackQuery):
    chat_id = int(callback.data.split(":")[1])
    db = await connect_db()
    user = await db.fetchrow("SELECT is_banned FROM users WHERE chat_id = $1", chat_id)
    if user is None:
        await db.close()
        await callback.answer("❌ User not found.")
        return
    else:
        await db.execute("UPDATE users SET is_banned = NOT is_banned WHERE chat_id = $1", chat_id)
        await db.close()
        await list_users(callback.message, page=1)
        await callback.answer("✅ User banned." if user['is_banned'] else "✅ User unbanned.")
