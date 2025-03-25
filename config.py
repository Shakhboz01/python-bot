import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
SUGGESTION_GROUP_ID = int(os.getenv("SUGGESTION_GROUP_ID", -1))
FORM_REQUEST_GROUP_ID = int(os.getenv("FORM_REQUEST_GROUP_ID", -1))
CALLBACK_REQUESTS_GROUP_ID = int(os.getenv("CALLBACK_REQUESTS_GROUP_ID", -1))
DB_CONFIG = {
    "database": os.getenv("DB_NAME", "default_db"),
    "user": os.getenv("DB_USER", "default_user"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}
