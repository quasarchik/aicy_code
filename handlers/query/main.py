from utils import texts, ai_api
from utils import util, log_bot
from database import DatabaseManager

from pyrogram import enums, Client, filters

def register_all_query_handlers(app: Client, db: DatabaseManager, log_warn):
    @app.on_callback_query(filters.regex("clear_data"))
    async def clear_data_handler(_, query):
        user_id = query.from_user.id
        
        # Clear the user's data history
        ai_api.all_data[user_id] = []
        
        # Send a confirmation message to the user
        await query.message.edit_text("История успешно очищена.", parse_mode=enums.ParseMode.MARKDOWN)
        
        # Optionally, remove the inline buttons after clearing
        await query.answer()  # Acknowledge the callback to remove loading state