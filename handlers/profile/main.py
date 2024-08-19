from datetime import datetime, timedelta
import ast, random

from database import DatabaseManager
from utils import texts
from utils import util, log_bot
from pyrogram import enums, Client, filters

def register_all_profile_handlers(app: Client, db: DatabaseManager, log_warn):

    @app.on_message(filters.command(['ник'], prefixes=['+', '-']))
    async def nick_change(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)
        text = " ".join(msg.text.split(' ')[1:])
        if text.strip() == "":
            db.update_data('users', 'id = ?', (msg.from_user.id,), custom_nickname=None)
            await msg.reply_text(texts.msg_nickname_deleted)
        elif not util.contains_invalid_characters(text):
            db.update_data('users', 'id = ?', (msg.from_user.id,), custom_nickname=text)
            await msg.reply_text(texts.msg_nickname_saved(text))
        else:
            await msg.reply_text(texts.msg_nickname_invalid(text))

    @app.on_message(filters.command(['пол'], prefixes=['+', '-']))
    async def gender_change(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)
        text = " ".join(msg.text.split(' ')[1:])
        
        if text.strip() == "":
            db.update_data('users', 'id = ?', (msg.from_user.id,), gender=None)
            await msg.reply_text(texts.msg_gender_deleted)
        else:
            gender = util.check_gender(text)
            
            if gender in ['М', 'Д']:
                # Save the nickname along with the gender
                gender = f"{text} ({gender})"
                db.update_data('users', 'id = ?', (msg.from_user.id,), gender=gender)
                await msg.reply_text(texts.msg_nickname_saved(gender))
            else:
                await msg.reply_text(texts.msg_gender_invalid(text))

    @app.on_message(filters.command(['др'], prefixes=['+', '-']))
    async def birthdate_change(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)
        text = " ".join(msg.text.split(' ')[1:])
        
        if text.strip() == "":
            # Если текст после команды пустой, удаляем дату рождения и возраст
            db.update_data('users', 'id = ?', (msg.from_user.id,), birthdate=None, age=None, zodiac=None)
            await msg.reply_text(texts.msg_birthdate_deleted)
        else:
            try:
                # Попробуем распарсить дату
                birthdate = datetime.strptime(text, '%d.%m.%Y')  # Измените формат по необходимости
                today = datetime.today()
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                
                # Определяем знак зодиака
                zodiac = util.get_zodiac_sign(birthdate.day, birthdate.month)
                
                # Обновляем данные в базе данных
                db.update_data('users', 'id = ?', (msg.from_user.id,), birthdate=birthdate.date(), age=age, zodiac=zodiac)
                await msg.reply_text(texts.msg_birthdate_saved(age, zodiac))
            except ValueError:
                await msg.reply_text(texts.msg_birthdate_invalid)

    @app.on_message(filters.command(['город'], prefixes=['+', '-']))
    async def city_change(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)

        text = " ".join(msg.text.split(' ')[1:])
        if text.strip() == "":
            db.update_data('users', 'id = ?', (msg.from_user.id,), city=None)
            await msg.reply_text(texts.msg_nickname_deleted)
        elif not util.contains_invalid_characters(text):
            db.update_data('users', 'id = ?', (msg.from_user.id,), city=text)
            await msg.reply_text(texts.msg_city_saved(text))
        else:
            await msg.reply_text(texts.msg_city_invalid(text))

    @app.on_message(filters.command(['мой'], prefixes=['']))
    async def get_profile_info(_, msg):
        await util.check_user(db, msg)
        await log_bot(msg)
        text = " ".join(msg.text.split(' ')[1:])
        users = db.find_by_column('users', 'id', msg.from_user.id)
        if users:
            user = users[0]
            name = util.get_user_name(user)
            if text == 'город':
                await msg.reply_text(texts.get_my_data_city(name, user['city']))
            elif text == 'др':
                await msg.reply_text(texts.get_my_data_dr(name, user['birthdate'], user['age'], user['zodiac']))
            elif text == 'ник':
                await msg.reply_text(texts.get_my_data_nick(name, user['custom_nickname'] if user['custom_nickname'] else "не указан("))
            elif text == 'пол':
                await msg.reply_text(texts.get_my_data_gender(name, user['gender'] if user['gender'] else "не указан("))
            else:
                await msg.reply_text(texts.invalid_get_my_data)