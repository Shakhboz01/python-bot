from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from admin.keyboads import ticket_actions_keyboard, unsolved_tickets_keyboard
from admin.states.admin_chat_state import AdminChatState
from database import connect_db, get_chats, create_outgoing_chat
from middlewares.admin_check import AdminCheckMiddleware

router = Router()
router.message.middleware(AdminCheckMiddleware())

@router.message(F.text.lower() == 'unsloved tickets')
async def show_unsolved_tickets(message: Message):
    db = await connect_db()
    tickets = await db.fetch("SELECT id, user_id FROM tickets WHERE solved = FALSE")
    await db.close()

    if not tickets:
        await message.answer("✅ No unsolved tickets found.")
        return

    await message.answer("📝 Unsolved Tickets:", reply_markup=unsolved_tickets_keyboard(tickets))

@router.callback_query(F.data.startswith("ticket:"))
async def ticket_actions(callback: CallbackQuery):
    ticket_id = int(callback.data.split(":")[1])
    await callback.message.answer(
        f"Ticket #{ticket_id} Actions:",
        reply_markup=ticket_actions_keyboard(ticket_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mark_solved:"))
async def mark_ticket_solved(callback: CallbackQuery):
    ticket_id = int(callback.data.split(":")[1])
    db = await connect_db()
    await db.execute("UPDATE tickets SET solved = TRUE WHERE id = $1", ticket_id)
    await db.close()

    await callback.message.answer(f"✅ Ticket #{ticket_id} has been marked as solved.")
    await callback.answer()


@router.callback_query(F.data.startswith("show_chats:"))
async def show_ticket_chats(callback: CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.split(":")[1])
    db = await connect_db()
    chats = await get_chats(ticket_id)
    await db.close()

    if not chats:
        await callback.message.answer("💬 No chats found for this ticket.")
        await callback.answer()
        return

    # Display all chats
    chat_history = "\n".join(
        [f"{'👤 User' if chat['incoming'] else '🛠 Admin'}: {chat['message']}" for chat in chats]
    )
    await callback.message.answer(f"💬 Chat History for Ticket #{ticket_id}:\n\n{chat_history}")

    # Set FSM state for sending a message
    await state.update_data(ticket_id=ticket_id)
    await state.set_state(AdminChatState.sending_message)
    await callback.message.answer("✍️ Type your message to send to the user:")
    await callback.answer()
