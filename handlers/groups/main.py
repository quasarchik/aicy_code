from database import DatabaseManager
from utils import util

from pyrogram import enums, Client, filters


def register_all_group_handlers(app: Client, db: DatabaseManager, log_bot, log_warn):
    @app.on_message(~filters.private & filters.command(['топ'], prefixes=['!', '', '/', '.', 'айси ', 'айсочка ']))
    async def top_chat(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        log_bot(msg)
        