from database import DatabaseManager
from utils import util, ai_api
from utils.config import ADMIN_ID, GROQ_API
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram import enums, Client, filters
from utils import texts, log_bot

from random import choice
import sympy as sp
import ast
from datetime import datetime, timedelta



def register_all_group_handlers(app: Client, db: DatabaseManager, log_warn):
    @app.on_message(~filters.private & filters.command(['топ'], prefixes=['!', '', '/', '.', 'айси ', 'айсочка ']))
    async def top_chat(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)

    @app.on_message(filters.command(['start']) & ~filters.private)
    async def start_group(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)

        async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.RECENT):
            await util.check_user_id(db, m)

        await app.send_sticker(
            chat_id=msg.chat.id,  # ID чата, куда отправляем стикер
            sticker=texts.stickers[choice(['bang', 'love', 'socutie', 'dance', 'cutie', ])],
            protect_content=True
        )       
        await msg.reply_text(texts.greeting_group)

        
    @app.on_message(filters.new_chat_members)
    async def on_new_member(client, msg):
        await util.check_group(db, msg)
        for new_member in msg.new_chat_members:
            if new_member.is_self:
                log_warn("NEW CHAT ADDED ME!!!")
                await msg.reply(texts.new_chat_added("https://teletype.in/@aicy_docs/aicy_08_08_24"))
            else:
                log_warn("In chat new member")

    @app.on_message(~filters.private & filters.command(['айси', 'айсочка'], prefixes=['!', '', '/', '.']))
    async def aicy_handler(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
        
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

        else:
            text = msg.text
            user_id = msg.from_user.id

            # Add the user's message to the data history
            ai_api.add_to_data(user_id, "user", text)

            # Generate the response from the AI
            response_content = ai_api.chat_response(text, ai_api.all_data.get(user_id, []), ai_api.client)

            # Add the AI's response to the data history
            add_data = ai_api.add_to_data(user_id, "assistant", response_content)

            # Check if the add_data is 0
            if add_data == 0:
                # Create an inline button for clearing the all_data
                clear_button = InlineKeyboardButton("Очистить историю", callback_data="clear_data")
                reply_markup = InlineKeyboardMarkup([[clear_button]])
                
                # Send the response to the user with the inline button
                await msg.reply(response_content, reply_markup=reply_markup, parse_mode=enums.ParseMode.MARKDOWN)
            else:
                # Send the response to the user without the inline button
                await msg.reply(response_content, parse_mode=enums.ParseMode.MARKDOWN)

    @app.on_message(~filters.private & filters.command(['шип', 'пейринг'], prefixes=['!', '', '/', '.', "айси ", "айсочка "]))
    async def pairing_handler(_, msg):
        await util.check_user(db, msg)
        await util.check_group(db, msg)
        await log_bot(msg)
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
        await log_bot(msg)
        group = db.find_by_column('groups', 'id', msg.chat.id)
        if group:
            group = group[0]
            stats = ast.literal_eval(group[0]['stat'])
            stats = dict(sorted(stats.items(), key=lambda item: item[1]))
            c = 1
            for key, value in stats.items():
                user = db.find_by_column('users', 'id', key)[0]
                text += f"{c}. {util.get_user_name(user)} — {value}"