from utils.config import ADMIN_ID
from pyrogram import errors, filters, Client, types
from utils import texts, util, log_bot
from database import DatabaseManager

def register_all_admin_handlers(app: Client, db: DatabaseManager, log_warn):

    @app.on_message(filters.command(['set'], prefixes=["/", "!", ".", '']))
    async def set_admin(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        text = " ".join(msg.text.split(' ')[1:])
        text = text.split(' ')

        if len(text) < 4:
            await msg.reply_text("Не верный формат команды")
            return

        table, how, column, value, *args = text
        if how == 'all':
            # Update all rows in the specified column
            if len(text) == 4:
                table, how, column, value = text
                if value == 'null':
                    value = None
                data = {column: value}
                db.update_data(table, '1=1', (), **data)  # '1=1' is a tautology that matches all rows
                await msg.reply_text(f"Обновлено значение столбца '{column}' на '{value}' для всех записей в таблице '{table}'")
            else:
                await msg.reply_text("Не верный формат команды. Используйте '/set <table> all <column> <value>'")
        else:
            if len(text) == 5:
                how, who, what, value = text[1:]
                data = {what: value}
                db.update_data(table, f'{how} = ?', (who,), **data)
                await msg.reply_text("строка обработана\n" + "\n".join(f"{key} : {value}" for key, value in data.items()))
            else:
                await msg.reply_text("Не верный формат команды. Используйте '/set <table> <how> <who> <what> <value>'")

    @app.on_message(filters.command(['del'], prefixes=["/", "!", ".", '']))
    async def del_admin(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        text = " ".join(msg.text.split(' ')[1:])
        text = text.split(' ')

        if len(text) == 3:
            table, how, who = text
            db.delete_data(table, f'{how} = ?', (who,))
            await msg.reply_text("строка обработана\n" + " ".join([table, how, who]))
        else:
            await msg.reply_text("Не верный формат команды")

    @app.on_message(filters.command(['id'], prefixes=["/", "!", ".", '']))
    async def id_admin(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        text = texts.get_info_chat(msg)
        await msg.reply_text(text)

    @app.on_message(filters.private & filters.command(['анонс'], prefixes=["."]))
    async def anonses(client, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        # Получаем ID чата из сообщения, если он указан
        parts = msg.text.split('\n')
        if len(parts) < 3:
            return
        chat_id = parts[1] if parts[1].lower() != 'all' else None  # Первый элемент после команды
        text = "\n".join(parts[2:]) if len(parts) > 2 else "\n".join(parts[1:])  # Сообщение, начиная со второго элемента

        users = db.fetch_data('users')
        groups = db.fetch_data('groups')

        msg_text = f"Отправляю сообщение {len(users)} пользователям и {len(groups)} группам!"
        message = await msg.reply_text(msg_text)

        if chat_id:  # Если chat_id указан, отправляем только в него
            try:
                await client.send_message(chat_id, text)
                msg_text += f"\n\nСообщение отправлено в чат с ID {chat_id}!"
            except Exception as e:
                msg_text += f"\n\nОшибка при отправке в чат с ID {chat_id}: {e}"
        else:  # Если chat_id не указан, отправляем всем пользователям и группам
            c = 0
            for user in users:
                try:
                    chat = await client.get_chat(user['id'])
                    if user['id'] != int(ADMIN_ID):
                        await client.send_message(user['id'], text)
                        c += 1
                except:
                    pass
            msg_text += f"\n\nОтправлено {c} пользователям!"
            
            c = 0
            for group in groups:
                try:
                    chat = await client.get_chat(group['id'])
                    await client.send_message(group['id'], text)
                    c += 1
                except:
                    pass
            msg_text += f"\n\nОтправлено {c} группам!"

        await message.edit_text(msg_text)
        
    @app.on_message(filters.private & filters.command(['data'], prefixes=["."]))
    async def request_database(client, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        message = await client.send_message(
            chat_id=msg.chat.id,
            text="Подождите немного, загружаю документ... ⏳"
        )

        # Путь к файлу, который вы хотите отправить
        file_path = "aicy.db"
        await client.send_document(
            chat_id=msg.chat.id,  # ID чата, куда отправляется файл
            document=file_path,       # Путь к файлу
            caption="Вот ваш файл 📄",  # Подпись к файлу
        )
        await client.delete_messages(
            chat_id=msg.chat.id,
            message_ids=message.id
        )
     
    @app.on_message(filters.private & filters.command(['logs'], prefixes=["."]))
    async def request_logs(client, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1
        message = await client.send_message(
            chat_id=msg.chat.id,
            text="Подождите немного, загружаю документ... ⏳"
        )

        # Путь к файлу, который вы хотите отправить
        file_path = "aicy.log"
        await client.send_document(
            chat_id=msg.chat.id,  # ID чата, куда отправляется файл
            document=file_path,       # Путь к файлу
            caption="Вот ваш файл 📄",  # Подпись к файлу
        )
        await client.delete_messages(
            chat_id=msg.chat.id,
            message_ids=message.id
        )
    