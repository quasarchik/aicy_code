from datetime import datetime, timedelta
import ast, random
import re

from utils import texts
from utils import util, log_bot
from database import DatabaseManager

from pyrogram import enums, Client, filters


async def handle_user_action(msg, log_warn, db, util, action, unit, min_value, max_value, cooldown_hours, already_msg, grow_msg, shrink_msg):
    await util.check_user(db, msg)
    await log_bot(msg)
    users = db.find_by_column('users', 'id', msg.from_user.id)
    if users:
        user = users[0]
        name = util.get_user_name(user)
        timers = ast.literal_eval(user['timers'])
        cur_timer = timers.get(action)
        current_date = datetime.now()
        
        if cur_timer:
            last_date = datetime.strptime(cur_timer, '%Y-%m-%d %H:%M:%S')
            cooldown_duration = timedelta(hours=cooldown_hours)
            if current_date < last_date + cooldown_duration:
                remaining_time = last_date + cooldown_duration - current_date
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await msg.reply_text(already_msg(name, user[action], remaining_time.days, hours, minutes, seconds))
                return
        
        added = random.randint(min_value, max_value)
        current_value = user[action] if user[action] else 0
        new_value = current_value + added
        timers[action] = current_date.strftime('%Y-%m-%d %H:%M:%S')
        db.update_data('users', 'id = ?', (user['id'],), **{action: new_value, 'timers': str(timers)})
        
        if added >= 0:
            await msg.reply_text(grow_msg(name, added, new_value))
        else:
            await msg.reply_text(shrink_msg(name, added, new_value))
    else:
        log_warn(f"User not found in the database. {msg.from_user.id}")

def register_all_module_handlers(app: Client, db: DatabaseManager, log_warn):
    @app.on_message(filters.command(['cock'], prefixes=["!", ".", '']))
    async def dick_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util,
            'dick', 
            'см', 
            -20, 
            40, 
            24,  # Cooldown in hours
            texts.msg_already_played, 
            texts.msg_grew, 
            texts.msg_shrank
        )
    @app.on_message(filters.command(['beer'], prefixes=["/", "!", ".", '']))
    async def beer_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util, 
            'beer', 
            'кружек пива', 
            1, 
            20, 
            12,  # Cooldown in hours
            texts.msg_already_had_beer, 
            texts.msg_drunk_beer, 
            texts.msg_drunk_beer
        )
    @app.on_message(filters.command(['coffee'], prefixes=["/", "!", ".", '']))
    async def coffee_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util, 
            'coffee', 
            'кружек кофе', 
            1, 
            20, 
            12,  # Cooldown in hours
            texts.msg_already_had_coffee, 
            texts.msg_drunk_coffee, 
            texts.msg_drunk_coffee
        )
    @app.on_message(filters.command(['kymyz'], prefixes=["/", "!", ".", '']))
    async def kymyz_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util, 
            'kymyz', 
            'чашек кымыза', 
            1, 
            20, 
            12,  # Cooldown in hours
            texts.msg_already_had_kymyz, 
            texts.msg_drunk_kymyz, 
            texts.msg_drunk_kymyz
        )
    @app.on_message(filters.command(['tea'], prefixes=["/", "!", ".", '']))
    async def tea_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util, 
            'tea', 
            'кружек чая', 
            1, 
            20, 
            12,  # Cooldown in hours
            texts.msg_already_had_tea, 
            texts.msg_drunk_tea, 
            texts.msg_drunk_tea
        )
    @app.on_message(filters.command(["ферма", "фарма", "мани"], prefixes=["/", "!", ".", '']))
    async def farm_handler(_, msg):
        await util.check_group(db, msg)
        await handle_user_action(
            msg, log_warn, db, util, 
            'coins', 
            'монет', 
            10, 
            400, 
            8,  # Cooldown in hours
            texts.msg_already_farm_coins, 
            texts.msg_farm_coins, 
            texts.msg_farm_coins
        )

    @app.on_message(filters.command(['пинг'], prefixes=['!', '', '/', '.']))
    async def ping(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
        
        await msg.reply_text("ПОНГ")
    @app.on_message(filters.command(['кинг'], prefixes=['!', '', '/', '.']))
    async def king(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)

        await msg.reply_text("КОНГ")
    @app.on_message(filters.command(['пью'], prefixes=['!', '', '/', '.']))
    async def piy(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)

        await msg.reply_text("ПАУ")
    @app.on_message(filters.command(['пиу'], prefixes=['!', '', '/', '.']))
    async def puy(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
        
        await msg.reply_text("ПАУ")
    @app.on_message(filters.command(['лол'], prefixes=['!', '', '/', '.']))
    async def lol(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
        
        await msg.reply_text("КЕК")
    @app.on_message(filters.command(['тик'], prefixes=['!', '', '/', '.']))
    async def tik(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
        
        await msg.reply_text("ТОК")
            
    @app.on_message(filters.command(['совмы'], prefixes=['!', '', '/', '.']) & filters.reply)
    async def birthdate_sovm(client, msg):
        await util.check_user(db, msg)
        await log_bot(msg)
        

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