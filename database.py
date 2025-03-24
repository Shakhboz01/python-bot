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
            is_banned BOOLEAN DEFAULT FALSE
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
