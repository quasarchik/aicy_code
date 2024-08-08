import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
LOG_CHAT = os.getenv("LOG_CHAT")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")