from .admin import register_all_admin_handlers
from .query import register_all_query_handlers
from .modules import register_all_module_handlers
from .profile import register_all_profile_handlers
from .groups import register_all_group_handlers
from .models import register_all_ai_handlers

from keyboards import inlines, keyboards
from utils import texts
from utils import util
from database import DatabaseManager

from pyrogram import enums, Client, filters


import os
import asyncio
import cv2
import numpy as np
import io
import ast
from datetime import timedelta, datetime
import sympy as sp
from random import choice, randint
import re



def register_all_handlers(app: Client, db: DatabaseManager, log_bot, log_warn):
    register_all_admin_handlers(app, db, log_bot, log_warn)
    register_all_query_handlers(app, db, log_bot, log_warn)
    register_all_module_handlers(app, db, log_bot, log_warn)
    register_all_profile_handlers(app, db, log_bot, log_warn)
    register_all_group_handlers(app, db, log_bot, log_warn)
    register_all_ai_handlers(app, db, log_bot, log_warn)

    @app.on_message(filters.command(['start']) & ~filters.private)
    async def start_group(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)

        async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.RECENT):
            await util.check_user_id(db, m)

        log_bot(msg)
        await app.send_sticker(
            chat_id=msg.chat.id,  # ID чата, куда отправляем стикер
            sticker=texts.stickers[choice(['bang', 'love', 'socutie', 'dance', 'cutie', ])],
            protect_content=True
        )       
        await msg.reply_text(texts.greeting_group)
    

    @app.on_message(filters.command(['start']) & filters.private)
    async def start_private(_, msg):
        user = await util.check_user(db, msg)
        log_bot(msg)

        await app.send_sticker(
            chat_id=msg.chat.id,  # ID чата, куда отправляем стикер
            sticker=texts.stickers[choice(['bang', 'love', 'socutie', 'dance', 'cutie'])],
            protect_content=True
        )
        
        await msg.reply_text(
            texts.greeting_private,
            reply_markup=keyboards.menu_kb
        )
    @app.on_message(filters.command(['меню', 'menu'], prefixes=['', '/', '.']) & filters.private)
    async def menu(_, msg):
        user = await util.check_user(db, msg)
        log_bot(msg)
        
        await msg.reply_text('Загружаю меню..📍',
            reply_markup=keyboards.menu_kb
        )
    
    @app.on_message(~filters.private & filters.command(['айси', 'айсочка'], prefixes=['!', '', '/', '.']))
    async def aicy_handler(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        log_bot(msg)
        
        if not msg.text:
            return

        text = " ".join(msg.text.split(' ')[1:]).strip().lower()

        if text.startswith(('кто', 'кого', 'кому')):
            # Обработка команд типа "айси кто", "айси кого", "айси кому" и т.д.
            await util.handle_who_command(app, msg, text, db)

        elif text.startswith(('шанс', 'вероятность')):
            # Обработка команд типа "айси шанс", "айси вероятность" и т.д.
            await util.handle_chance_command(app, msg, text, db)

        elif text.startswith(('данет', 'да или нет', 'ответь')):
            # Обработка команд типа "айси данет", "айси да или нет", "айси ответь" и т.д.
            await util.handle_yes_no_command(app, msg, text, db)
        elif text.startswith(('скажи')):
            text = " ".join(text.split(' ')[1:]).strip().lower()
            await msg.reply_text(f'Меня попросили сказать: {text}')
        elif text.startswith(('алг', 'алгебра')):
            text = " ".join(text.split(' ')[1:]).strip().lower()
            x, y = sp.symbols('x y')
            if text.startswith(('развернуть')):
                expr_str = " ".join(text.split(' ')[1:]).strip().lower()
                expr = sp.sympify(expr_str)
                res = sp.expand(expr)
                res = util.format_expression(res)
                await msg.reply_text(f'Результат: {res}')
            elif text.startswith(('упростить')):
                expr_str = " ".join(text.split(' ')[1:]).strip().lower()
                expr = sp.sympify(expr_str)
                res = sp.factor(expr)
                res = util.format_expression(res)
                await msg.reply_text(f'Результат: {res}')
            elif text.startswith(('решить')):
                expr_str = " ".join(text.split(' ')[1:]).strip().lower()
                lhs_str, rhs_str = expr_str.split('=')
                rhs_str = rhs_str.strip()  # Remove any leading/trailing whitespace

                # Convert the left-hand side and right-hand side to SymPy expressions
                lhs = sp.parse_expr(lhs_str)
                rhs = sp.parse_expr(rhs_str)

                expr = sp.Eq(lhs, rhs)

                res = sp.solve(expr, x)
                res = util.format_expression(res)
                await msg.reply_text(f'Результат: {res}')
            elif text.startswith(('дифф')):
                expr_str = " ".join(text.split(' ')[1:]).strip().lower()
                expr = sp.sympify(expr_str)
                res = sp.diff(expr, x)
                await msg.reply_text(f'Результат: {res}')
            elif text.startswith(('итегр')):
                expr_str = " ".join(text.split(' ')[1:]).strip().lower()
                expr = sp.sympify(expr_str)
                res = sp.integrate(expr, x)
                res = util.format_expression(res)
                await msg.reply_text(f'Результат: {res}')

        
    @app.on_message(~filters.private & filters.command(['шип', 'пейринг'], prefixes=['!', '', '/', '.', "айси ", "айсочка "]))
    async def pairing_handler(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        log_bot(msg)
        users = db.find_by_column('users', 'id', msg.from_user.id)
        if users:
            user = users[0]
            name = util.get_user_name(user)
            timers = ast.literal_eval(user['timers'])
            cur_timer = timers.get('pairing')
            current_date = datetime.now()
            
            if cur_timer:
                last_date = datetime.strptime(cur_timer, '%Y-%m-%d %H:%M:%S')
                cooldown_duration = timedelta(seconds=60)
                if current_date < last_date + cooldown_duration:
                    remaining_time = last_date + cooldown_duration - current_date
                    _, remainder = divmod(remaining_time.seconds, 3600)
                    _, seconds = divmod(remainder, 60)
                    await msg.reply_text(texts.msg_pairing_not_get(name, seconds))
                    return
            

            timers['pairing'] = current_date.strftime('%Y-%m-%d %H:%M:%S')
            db.update_data('users', 'id = ?', (user['id'],), **{'timers': str(timers)})

            await util.handle_pair_command(app, msg, db, texts)

    @app.on_message(~filters.private & filters.command(['топ'], prefixes=['!', '/', '.']))
    async def top_chat(client, msg):
        await util.check_user(db, msg)
        group = db.find_by_column('groups', 'id', msg.chat.id)
        if group:
            group = group[0]
            stats = ast.literal_eval(group[0]['stat'])
            stats = dict(sorted(stats.items(), key=lambda item: item[1]))
            c = 1
            for key, value in stats.items():
                user = db.find_by_column('users', 'id', key)[0]
                text += f"{c}. {util.get_user_name(user)} — {value}"



    @app.on_message(~filters.private & filters.command(['мульт'], prefixes=['!', '', '/', '.']) & filters.photo)
    async def mult_filter(client, msg):
        await util.check_user(db, msg)
        now = datetime.now()
        users = db.find_by_column('users', 'id', msg.from_user.id)
        user = users[0]
        # Check for timer
        timers = ast.literal_eval(user['timers'])
        timer = timers.get('multi')
        if timer:
            time_diff = now - datetime.fromisoformat(timer)
            cooldown = timedelta(seconds=60)
            if time_diff < cooldown:
                remaining_time = cooldown - time_diff
                await msg.reply_text(f"Подождите! Еще не прошло {remaining_time.seconds} секунд.")
                return

        await util.check_group(db, msg)
        log_bot(msg)

        # Update timer
        timers['multi'] = now.isoformat()
        db.update_data('users', 'id = ?', (msg.from_user.id,), timers=str(timers))  # Update the database with the new timer

        nsamples = 1
        nbilateral = 7

        photo_file = await msg.download()
        img_rgb = cv2.imread(photo_file)
        cartoonizer = util.Cartoonizer(numDownSamples=nsamples, numBilateralFilters=nbilateral)
        cartoon_image = cartoonizer.render(img_rgb)
        _, buffer = cv2.imencode('.jpg', cartoon_image)
        img_bytes = buffer.tobytes()
        with io.BytesIO(img_bytes) as photo:
            await msg.reply_photo(photo)

        os.remove(photo_file)

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



    async def handle_ivent(_, msg):
        # Implement the handler logic here
        pass

    async def handle_hab_bota(_, msg):
        # Implement the handler logic here
        pass

    async def handle_balans(_, msg):
        # Implement the handler logic here
        pass


    @app.on_message(filters.command(['совмы'], prefixes=['!', '', '/', '.']) & filters.reply)
    async def birthdate_sovm(client, msg):
        await util.check_user(db, msg)
        log_bot(msg)
        

        user1 = db.find_by_column('users', 'id', msg.from_user.id)
        user2 = db.find_by_column('users', 'id', msg.reply_to_message.from_user.id)  # Убедитесь, что второй пользователь правильный

        if user1 and user2:
            user1 = user1[0]
            user2 = user2[0]

            gender1, birthdate1 = user1['gender'], user1['birthdate']
            gender2, birthdate2 = user2['gender'], user2['birthdate']

            name1 = util.get_user_name(user1)
            name2 = util.get_user_name(user2)

            response = ''
            # Проверяем наличие гендеров
            if not gender1:
                response += f"{name1}, пожалуйста, укажите ваш пол!\n"
            if not gender2:
                response += f"{name2}, не указал пол(\n"
            # Проверяем наличие даты рождения
            if not birthdate1:
                response += f"{name1}, пожалуйста, установите вашу дату рождения\n"
            if not birthdate2:
                response += f"{name2}, не установил др(\n"

            if response:
                await msg.reply_text(response)
                return
            # Используем регулярные выражения для извлечения гендеров
            match1 = re.search(r'\((.*?)\)', gender1)
            match2 = re.search(r'\((.*?)\)', gender2)

            if match1 and match2:
                gender_value1 = match1.group(1)
                gender_value2 = match2.group(1)

                # Определяем, кто парень, а кто девушка
                if gender_value1 == "М":
                    user1_gender = "М"
                elif gender_value1 == "Д":
                    user1_gender = "Д"

                if gender_value2 == "М":
                    user2_gender = "М"
                elif gender_value2 == "Д":
                    user2_gender = "Д"

                if user1_gender == user2_gender:
                    user2_gender = "Д"
                    man_birthdate = birthdate1
                    woman_birthdate = birthdate2
                else:
                    if user1_gender == "М":
                        man_birthdate = birthdate1
                        woman_birthdate = birthdate2
                    else:
                        man_birthdate = birthdate2
                        woman_birthdate = birthdate1

                man_birthdate = f"{int(man_birthdate[8:10])}.{int(man_birthdate[5:7])}.{man_birthdate[:4]}"
                woman_birthdate = f"{int(woman_birthdate[8:10])}.{int(woman_birthdate[5:7])}.{woman_birthdate[:4]}"
                result = await util.sovms(man_birthdate, woman_birthdate)
                reply_text = f"Совместимость для {name1} и {name2}{texts.random_love_emoji()}\n\n{result}"
                await msg.reply_text(reply_text)

            else:
                await msg.reply("Не удалось определить гендер одного из пользователей.")
        else:
            await msg.reply("Пользователи не найдены.")


# Main handler
    @app.on_message(filters.text)
    async def main_handler(client, msg):
        await util.check_user(db, msg)
        log_bot(msg)

        # Check for specific commands and call the respective handler
        if msg.text in ["Анкета🌸", "анкета", "анкета", ".анкета", "/анкета"]:
            await handle_anketa(client, msg)
        elif msg.text in ["Команды🍭", "Команды", "команды", ".команды", "/команды"]:
            await handle_komandy(client, msg)
        elif msg.text in ["Разработчик🏵"] and msg.chat.id < 0:
            await handle_razrabotchik(client, msg)
        elif msg.text in ["РП-команды✨", "Рпшки", "рпшки", ".рпшки", "/рпшки"]:
            await handle_rp_komandy(client, msg)
        elif msg.text in ["Ивенты🌑", "Ивенты", "ивенты", ".ивенты", "/ивенты"]:
            await handle_ivent(client, msg)
        elif msg.text in ["Хаб бота🌕"] and msg.chat.id < 0:
            await handle_hab_bota(client, msg)
        elif msg.text in ["Баланс🌻", "Баланс", "баланс", ".баланс", "/баланс"]:
            await handle_balans(client, msg)
        elif msg.text.startswith('*') and msg.text.endswith('*') and msg.chat.id < 0:
            if msg.reply_to_message:
                await util.rp_command(app, msg, texts, db)
            else:
                await msg.reply_text("РП-Команды можно использовать ответом к сообщению собеседника!")