from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from database import connect_db
from admin.keyboads import user_list_keyboard
from middlewares.admin_check import AdminCheckMiddleware

router = Router()
router.message.middleware(AdminCheckMiddleware())
USERS_PER_PAGE = 10

@router.message(F.text == "Блокировать&Разблокировать пользователей")
async def list_users(message: Message, state=None, page=1):
    db = await connect_db()
    offset = (page - 1) * USERS_PER_PAGE
    users = await db.fetch(
        "SELECT chat_id, full_name, is_banned FROM users ORDER BY chat_id LIMIT $1 OFFSET $2",
        USERS_PER_PAGE, offset
    )
    await db.close()

    if not users:
        await message.answer("❌ Пользователи не найдены.")
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
        await callback.answer("❌ Пользователь не найден.")
        return
    else:
        await db.execute("UPDATE users SET is_banned = NOT is_banned WHERE chat_id = $1", chat_id)
        await db.close()
        await list_users(callback.message, page=1)
        await callback.answer("✅ Пользователь разблокирован." if user['is_banned'] else "✅ Пользователь заблокирован.")
