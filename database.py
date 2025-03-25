import asyncpg
from config import DB_CONFIG
import re

CYRILLIC_NAME_REGEX = re.compile(r"^[А-ЯЁа-яё]+ [А-ЯЁа-яё]+$")  # Full name (one space, Cyrillic)
PHONE_REGEX = re.compile(r"^\+7\d{10}$")


async def connect_db():
    return await asyncpg.connect(**DB_CONFIG)

async def create_table():
    db = await connect_db()
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone_number TEXT,
            is_banned BOOLEAN DEFAULT FALSE,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(chat_id),
            solved BOOLEAN DEFAULT FALSE
        )
    """)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            ticket_id INT REFERENCES tickets(id),
            incoming BOOLEAN DEFAULT TRUE,
            message TEXT
        )
    """)
    await db.close()

async def get_user(chat_id):
    db = await connect_db()
    user = await db.fetchrow("SELECT * FROM users WHERE chat_id = $1", chat_id)
    await db.close()
    return user

async def add_user(chat_id, full_name, phone_number):
    db = await connect_db()
    await db.execute(
        "INSERT INTO users (chat_id, full_name, phone_number) VALUES ($1, $2, $3)",
        chat_id, full_name, phone_number
    )
    await db.close()

async def update_full_name(chat_id, full_name):
    db = await connect_db()
    await db.execute(
        "UPDATE users SET full_name = $1 WHERE chat_id = $2;",
        full_name, chat_id
    )
    await db.close()

async def update_phone_number(chat_id, phone_number):
    db = await connect_db()
    await db.execute(
        "UPDATE users SET phone_number = $1 WHERE chat_id = $2;",
        phone_number, chat_id
    )
    await db.close()

# create incoming chat record for ticket
async def create_incoming_chat(chat_id, message_text):
    db = await connect_db()
    # Check for an unsolved ticket for the user
    ticket = await db.fetchrow(
        "SELECT id FROM tickets WHERE user_id = $1 AND solved = FALSE",
        chat_id
    )
    if not ticket:
        # Create a new ticket if none exists
        ticket_id = await db.fetchval(
            "INSERT INTO tickets (user_id) VALUES ($1) RETURNING id",
            chat_id
        )
    else:
        ticket_id = ticket['id']

    # Create an incoming chat record for the ticket
    await db.execute(
        "INSERT INTO chats (ticket_id, incoming, message) VALUES ($1, TRUE, $2)",
        ticket_id, message_text
    )
    await db.close()



# close any unsolved tickets of a user
async def close_tickets(chat_id):
    db = await connect_db()
    await db.execute(
        "UPDATE tickets SET solved = TRUE WHERE user_id = $1 AND solved = FALSE",
        chat_id
    )
    await db.close()

# create an chat sent from an admin(incoming = false), first check if there is an unsolved ticket for the user, if none return
async def create_outgoing_chat(chat_id, message_text):
    db = await connect_db()
    # Check for an unsolved ticket for the user
    ticket = await db.fetchrow(
        "SELECT id FROM tickets WHERE user_id = $1 AND solved = FALSE",
        chat_id
    )
    if not ticket:
        return

    # Create an outgoing chat record for the ticket
    await db.execute(
        "INSERT INTO chats (ticket_id, incoming, message) VALUES ($1, FALSE, $2)",
        ticket['id'], message_text
    )
    await db.close()


# get all chats for a ticket
async def get_chats(ticket_id):
    db = await connect_db()
    chats = await db.fetch("SELECT * FROM chats WHERE ticket_id = $1", ticket_id)
    await db.close()
    return chats

async def get_users():
    db = await connect_db()
    users = await db.fetch("SELECT * FROM users WHERE is_banned = FALSE AND is_admin = FALSE")
    await db.close()
    return users
