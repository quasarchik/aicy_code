from utils.config import ADMIN_ID
from pyrogram import errors, filters, Client
from utils import texts, util
from database import DatabaseManager

def register_all_admin_handlers(app: Client, db: DatabaseManager, log_bot, log_warn):

    @app.on_message(filters.command(['set'], prefixes=["/", "!", ".", '']))
    async def set_admin(_, msg):
        await util.check_user(db, msg)
        log_bot(msg)

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
        log_bot(msg)

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
        log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        text = texts.get_info_chat(msg)
        await msg.reply_text(text)

    @app.on_message(filters.command(['анонс'], prefixes=["."]))
    async def anonses(client, msg):
        await util.check_user(db, msg)
        log_bot(msg)

        if str(msg.from_user.id) != ADMIN_ID:
            return -1

        text = "\n".join(msg.text.split('\n')[1:])
        users = db.fetch_data('users')
        groups = db.fetch_data('groups')
        
        msg_text = f"Отправляю сообщение {len(users)} пользователям и {len(groups)} группам!"
        message = await msg.reply_text(msg_text)
        await msg.reply_text(text)
        c = 0
        for user in users:
            try:
                chat = await client.get_chat(user['id'])
                if user['id'] != int(ADMIN_ID):
                    await client.send_message(user['id'], text)
                    pass
                c += 1
            except:
                pass
        msg_text += f"\n\nОтправлено {c} пользователям!"
        await message.edit_text(msg_text)
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
        