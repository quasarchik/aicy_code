from pyrogram import Client, enums
from utils import BOT_TOKEN, API_ID, API_HASH
from utils import log_start, log_bot, log_warn
from handlers import register_all_handlers
from database import DatabaseManager

app = Client("my_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
app.set_parse_mode(enums.ParseMode.HTML)
db = DatabaseManager('aicy.db')

register_all_handlers(app, db, log_bot, log_warn)
app.send_sticker
def main():
    db.database_init(db, log_warn)
    log_start()

if __name__ == '__main__':
    app.run(main())