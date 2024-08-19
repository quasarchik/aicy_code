from .admin import register_all_admin_handlers
from .query import register_all_query_handlers
from .modules import register_all_module_handlers
from .profile import register_all_profile_handlers
from .groups import register_all_group_handlers
from .menu import register_all_menu_handlers

from keyboards import inlines, keyboards
from utils import texts, ai_api
from utils import util, log_bot
from database import DatabaseManager

from pyrogram import Client, filters

from random import choice


handlers = [
        register_all_admin_handlers,
        register_all_query_handlers,
        register_all_module_handlers,
        register_all_profile_handlers,
        register_all_group_handlers,
        register_all_menu_handlers
    ]

def register_all_handlers(app: Client, db: DatabaseManager, log_warn):
    """
    Регистрирует все обработчики для приложения.

    :param app: Клиент Pyrogram.
    :param db: Менеджер базы данных.
    :param log_warn: Функция для логирования предупреждений.
    """
    
    for handler in handlers:
        handler(app, db, log_warn)

    @app.on_message(filters.command(['start']) & filters.private)
    async def start_private(_, msg):
        user = await util.check_user(db, msg)
        await log_bot(msg)

        await app.send_sticker(
            chat_id=msg.chat.id,  # ID чата, куда отправляем стикер
            sticker=texts.stickers[choice(['bang', 'love', 'socutie', 'dance', 'cutie'])],
            protect_content=True
        )
        
        await msg.reply_text(
            texts.greeting_private,
            reply_markup=keyboards.menu_kb
        )