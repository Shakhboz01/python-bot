from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from admin.keyboads import ticket_actions_keyboard, unsolved_tickets_keyboard
from database import connect_db, get_chats, create_outgoing_chat
from middlewares.admin_check import AdminCheckMiddleware

class AdminChatState(StatesGroup):
    sending_message = State()

router = Router()

@router.message(AdminChatState.sending_message)
async def send_message_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get("ticket_id")

    # Get the user ID associated with the ticket
    db = await connect_db()
    ticket = await db.fetchrow("SELECT user_id FROM tickets WHERE id = $1", ticket_id)
    await db.close()

    if not ticket:
        await message.answer("❌ Ticket not found.")
        await state.clear()
        return

    user_id = ticket["user_id"]

    # Send the message to the user
    await message.bot.send_message(user_id, f"🛠 Admin: {message.text}")

    # Save the message as an outgoing chat
    await create_outgoing_chat(user_id, message.text)

    await message.answer("✅ Your message has been sent to the user.", reply_markup=ticket_actions_keyboard(ticket_id))
    await state.clear()