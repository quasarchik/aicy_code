from utils import texts
from utils import util, log_bot
from database import DatabaseManager

from pyrogram import enums, Client, filters
from keyboards import keyboards, inlines

def register_all_menu_handlers(app: Client, db: DatabaseManager, log_warn):
    @app.on_message(filters.command(['меню', 'menu'], prefixes=['', '/', '.']) & filters.private)
    async def menu(_, msg):
        user = await util.check_user(db, msg)
        await log_bot(msg)
        
        await msg.reply_text('Загружаю меню..📍',
            reply_markup=keyboards.menu_kb
        )

    # Define individual handler functions
    async def handle_anketa(_, msg):
        user = db.find_by_column('users', 'id', msg.from_user.id)
        if user:
            user = user[0]
            name = util.get_user_name(user)
            age = user['age']
            city = user['city']
            birthdate = user['birthdate']
            when_added = user['when_added']
            vip = user['vip']
            relationship = user['relationship']

            text  = f"Анкета {name}:\n"
            text += f"Город: {city if city else 'Не указан('}:\n"
            text += f"ДР: {birthdate if birthdate else 'Не указан'} ({age} лет)\n"
            text += f"Когда добавлен: {when_added}\n"
            text += f"Випка: {vip if vip else 'пока не получил випку'}\n"
            text += f"Отношения: {relationship if relationship != '{}' else 'Нету'}\n" 

            if msg.chat.id > 0:
                photos = []
                async for photo in app.get_chat_photos(msg.chat.id):
                    photos.append(photo)
                    break

                if len(photos) > 0:
                    # Получаем самую последнюю фотографию
                    photo = photos[0]

                    # Отправляем фотографию пользователю
                    await app.send_photo(chat_id=msg.chat.id, photo=photo.file_id, caption=text)
                else:
                    await app.send_photo(chat_id=msg.chat.id, photo=f'https://picsum.photos/seed/{msg.from_user.id}/600/?blur', caption=text)
            else:
                await app.send_photo(chat_id=msg.chat.id, photo=f'https://picsum.photos/seed/{msg.from_user.id}/600/?blur', caption=text)


    async def handle_komandy(_, msg):
        url = 'https://teletype.in/@aicy_docs/aicy_08_08_24'
        await app.send_message(msg.chat.id, f'Команды AICY | Amethyst Light\n{url}')

    async def handle_razrabotchik(_, msg):
        # Implement the handler logic here
        pass

    async def handle_rp_komandy(_, msg):
        user = db.find_by_column('users', 'id', msg.from_user.id)
        if user:
            user = user[0]
            name = util.get_user_name(user)
            text = f"{name},\n\nРолевая команда используется в ролевых играх (РП) для выражения действий персонажа или игрока.\n"
            text += "Она позволяет участникам игры описывать, что именно их персонаж делает в определённый момент времени, добавляя больше живости и интерактивности к игре.\n\n"
            text += "Примеры использования:\n"
            text += "  <i>*обнять*</i>\n"
            text += "  <i>*поцеловать*</i>\n"
            text += "  <i>*приступить к занятиям*</i>\n"
            text += "\nРП-Команд очень много!) Сможете найти все?"

            await msg.reply_text(text)

    async def handle_hab_bota(_, msg):
        # Implement the handler logic here
        pass

    async def handle_balans(_, msg):
        # Implement the handler logic here
        pass


    # Main handler
    @app.on_message(filters.text)
    async def main_handler(client, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        # Check for specific commands and call the respective handler
        if msg.text in ["Анкета🌸", "анкета", "анкета", ".анкета", "/анкета"]:
            await handle_anketa(client, msg)
        elif msg.text in ["Команды🍭", "Команды", "команды", ".команды", "/команды"]:
            await handle_komandy(client, msg)
        elif msg.text in ["Разработчик🏵"] and msg.chat.id < 0:
            await handle_razrabotchik(client, msg)
        elif msg.text in ["РП-команды✨", "Рпшки", "рпшки", ".рпшки", "/рпшки"]:
            await handle_rp_komandy(client, msg)
        elif msg.text in ["Хаб бота🌕"] and msg.chat.id < 0:
            await handle_hab_bota(client, msg)
        elif msg.text in ["Баланс🌻", "Баланс", "баланс", ".баланс", "/баланс"]:
            await handle_balans(client, msg) 
        elif msg.text.startswith('*') and msg.text.endswith('*') and msg.chat.id < 0:
            if msg.reply_to_message:
                await util.rp_command(app, msg, texts, db)
            else:
                await msg.reply_text("РП-Команды можно использовать ответом к сообщению собеседника!")