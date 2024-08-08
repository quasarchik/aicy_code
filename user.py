import asyncio
from pyrogram import Client, filters, idle
from utils import BOT_TOKEN, API_ID, API_HASH
from utils import texts, log_start, log_bot, log_warn, util
from handlers import register_all_handlers
from database import DatabaseManager

app = Client("my_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)

@app.on_message()
def hello(client, message):
    message.reply("hi")


app.run()