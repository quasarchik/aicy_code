import ast
import re
from utils.logs import log_warn
import time
from random import randint, seed, choice, shuffle
import numpy as np
import yt_dlp
import requests
from bs4 import BeautifulSoup
from pyrogram import enums
from utils import texts
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoFileClip

async def write_intel_data(db, msg):
    if msg.text is None or msg.reply_to_message is None or msg.reply_to_message.text is None and not msg.via_bot:
        return -1   
    input_text = msg.reply_to_message.text
    input_id = id(input_text)
    output_text = msg.text
    output_id = id(output_text)

    db.insert_data('intel',
        input_text=input_text,
        input_id=input_id,
        output_text=output_text,
        output_id=output_id,
    )
    #log_warn(f"INTEL SAVED - input:{input_text.replace('\n', ';')}:{input_id} | output:{output_text.replace('\n', ';')}:{output_id}")
    return 0
    
class main:
    class Cartoonizer:
        def __init__(self, numDownSamples=1, numBilateralFilters=7):
            self.numDownSamples = numDownSamples
            self.numBilateralFilters = numBilateralFilters

        def render(self, img_rgb):

            # downsample image using Gaussian pyramid
            img_color = img_rgb
            for _ in range(self.numDownSamples):
                img_color = cv2.pyrDown(img_color)
            # repeatedly apply small bilateral filter instead of applying
            # one large filter
            for _ in range(self.numBilateralFilters):
                img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
            # upsample image to original size
            for _ in range(self.numDownSamples):
                img_color = cv2.pyrUp(img_color)
            # convert to grayscale and apply bilateral blur
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            for _ in range(self.numBilateralFilters):
                img_gray_blur = cv2.bilateralFilter(img_gray, 9, 9, 7)
            # detect and enhance edges
            img_edge = cv2.adaptiveThreshold(img_gray_blur, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 9, 5)
            # convert back to color so that it can be bit-ANDed with color image
            img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
            #Ensure that img_color and img_edge are the same size, otherwise bitwise_and will not work
            height = min(len(img_color), len(img_edge))
            width = min(len(img_color[0]), len(img_edge[0]))
            img_color = img_color[0:height, 0:width]
            img_edge = img_edge[0:height, 0:width]
            return cv2.bitwise_and(img_color, img_edge)
    
    async def check_user(db, msg):
        await write_intel_data(db, msg)
        user = db.find_by_column('users', 'id', msg.from_user.id)
        
        if user:
            user = user[0]
            db.update_data('users', 'id = ?', (msg.from_user.id,), 
                        username=msg.from_user.username,
                        first_name=msg.from_user.first_name,
                        last_name=msg.from_user.last_name,
                        language_code=msg.from_user.language_code,
                        spam=datetime.now()
                        )
            
        else:
            
            db.insert_data('users', 
                        id=msg.from_user.id, 
                        username=msg.from_user.username,
                        first_name=msg.from_user.first_name,
                        last_name=msg.from_user.last_name,
                        language_code=msg.from_user.language_code,
                        age=0,
                        birthdate='1000-01-01',
                        when_added=datetime.now(),
                        coins=0,
                        amethysts=0,
                        vip=False,
                        relationship='{}',
                        characters='{}',
                        rp='{}',
                        dick=0,
                        tea=0,
                        beer=0,
                        coffee=0,
                        energy=0,
                        timers='{}',
                        spam=datetime.now()
                        )
            
        group = db.find_by_column('groups', 'id', msg.chat.id)
        user = db.find_by_column('users', 'id', msg.from_user.id)[0]

        if group:
            if user['id'] not in ast.literal_eval(group[0]['members']):
                members = ast.literal_eval(group[0]['members'])
                members[user['id']] = {}
                db.update_data('groups', 'id = ?', (msg.chat.id,), 
                        members=str(members), 
                        )

            top = ast.literal_eval(group[0]['stat'])
            if top.get(msg.from_user.id):
                top[msg.from_user.id] += 1
                db.update_data('groups', 'id = ?', (msg.chat.id,), 
                        stat=str(top), 
                        )
            else:
                top[msg.from_user.id] = 1
                db.update_data('groups', 'id = ?', (msg.chat.id,), 
                        stat=str(top), 
                        )
    async def check_user_id(db, user):
        user_d = db.find_by_column('users', 'id', user.user.id)
        if user_d:
            db.update_data('users', 'id = ?', (user.user.id,), 
                        username=user.user.username,
                        first_name=user.user.first_name,
                        last_name=user.user.last_name,
                        language_code=user.user.language_code,)
        else:
            db.insert_data('users', 
                        id=user.user.id, 
                        username=user.user.username,
                        first_name=user.user.first_name,
                        last_name=user.user.last_name,
                        language_code=user.user.language_code,
                        age=0,
                        birthdate='1000-01-01',
                        coins=0,
                        amethysts=0,
                        vip=False,
                        relationship='{}',
                        characters='{}',
                        rp='{}',
                        dick=0,
                        tea=0,
                        beer=0,
                        coffee=0,
                        energy=0,
                        timers='{}'
                        )
            
    async def check_group(db, msg):
        if msg.chat.id >= 0:
            return -1
        group = db.find_by_column('groups', 'id', msg.chat.id)
        if group:
            db.update_data('groups', 'id = ?', (msg.chat.id,), 
                    title=msg.chat.title, 
                    dscription=msg.chat.description, 
                    invite_link=msg.chat.invite_link, 
                    )
        else:
            db.insert_data('groups', 
                    id=msg.chat.id, 
                    title=msg.chat.title, 
                    dscription=msg.chat.description, 
                    invite_link=msg.chat.invite_link, 
                    status='neutral',
                    members='{}',
                    permissions='{}',
                    stat='{}'
                    )
            
    async def clear_text(commands, prefixes, msg):
        full_text = msg.text
        pattern = re.compile(r'^(?:' + '|'.join(re.escape(prefix) + re.escape(command) for prefix in prefixes for command in commands) + r')\b\s*', re.IGNORECASE)
        text_without_command = re.sub(pattern, '', full_text, count=1).strip()

        return text_without_command

    async def get_users(bot, chat_id: int, db) -> list[int]:
        # Получаем всех пользователей из базы данных
        users = db.fetch_data('users')

        matching_user_ids = []

        for user in users:
            chats = user.get('chats')
            if chats:
                chats = ast.literal_eval(chats)
                if chat_id in chats:
                    try:
                        chat_member = await bot.get_chat_member(chat_id, user['id'])
                        # Проверяем статус пользователя в чате
                        if chat_member.status in ['member', 'administrator', 'creator']:
                            matching_user_ids.append(user['id'])
                        else:
                            chats.pop(chat_id)
                            db.update_data('users', 'id = ?', (user,), chats=chats)
                    except Exception as e:
                        print(f"Error checking chat member status: {e}")
                        
        return matching_user_ids
    
    def get_zodiac_sign(day, month):
        if (month == 3 and day >= 21) or (month == 4 and day <= 20):
            return "Овен"
        elif (month == 4 and day >= 21) or (month == 5 and day <= 20):
            return "Телец"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
            return "Близнецы"
        elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
            return "Рак"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 23):
            return "Лев"
        elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
            return "Дева"
        elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
            return "Весы"
        elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
            return "Скорпион"
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return "Стрелец"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 20):
            return "Козерог"
        elif (month == 1 and day >= 21) or (month == 2 and day <= 20):
            return "Водолей"
        elif (month == 2 and day >= 21) or (month == 3 and day <= 20):
            return "Рыбы"
        return "Неизвестно"

    # Функция для получения имени пользователя
    def get_user_name(user):
        if user['custom_nickname']:
            return f'<a href="tg://user?id={user["id"]}">{user["custom_nickname"]}</a>'
        else:
            if user['last_name']:
                return f'<a href="tg://user?id={user["id"]}">{user["first_name"]} {user["last_name"]}</a>'
            else:
                return f'<a href="tg://user?id={user["id"]}">{user["first_name"]}</a>'

    def contains_invalid_characters(text):
        # Регулярное выражение для разрешённых символов
        allowed_chars_pattern = re.compile(r'^[А-Яа-яA-Za-z0-9]+$')
        
        # Проверяем, соответствует ли весь текст разрешённым символам
        if allowed_chars_pattern.match(text):
            return False
        else:
            return True

        
    def replace_pronouns(text):
        # Функция для замены местоимений
        def replacement(match):
            if match.group(0) == "я":
                return "вы"
            elif match.group(0) == "меня":
                return "вас"
            elif match.group(0) == "тебя":
                return "меня"
            elif match.group(0) == "c`тобой":
                return "со мной"
            elif match.group(0) == "cо`мной":
                return "с вами"
            
            return match.group(0)

        # Заменяем местоимения
        text = re.sub(r'\b(я|меня|тебя|с`тобой|со`мной)\b', replacement, text.replace(" ", "`"))
        
        return text.replace("`", " ")


    async def handle_who_command(app, msg, text, db):
        seed(100*time.time() * msg.from_user.id)
        members = []
        async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.RECENT):
            if db.exists('users', 'id', m.user.id):
                members.append(m.user.id)

        member = choice(members)
        user = db.find_by_column('users', 'id', member)
        if not user:
            main.check_user(db, msg)
            user = db.find_by_column('users', 'id', member)
        name = main.get_user_name(user[0])
        text = " ".join(text.split(' ')[1:]).strip().lower()
        text = main.replace_pronouns(text)
        phrase = choice(texts.phrases)
        res = f"{phrase} {name} {text}"
        await msg.reply_text(res)
        
    def format_expression(expr):
        expr_str = str(expr)

        expr_str = expr_str.replace('*', '')
        expr_str = expr_str.replace('**', '^')
        superscripts = {
            '2': '²', '3': '³', '4': '⁴', '5': '⁵',
            '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }

        for num, superscript in superscripts.items():
            expr_str = expr_str.replace(f'^{num}', superscript)

        expr_str = expr_str.replace('sqrt', '√')

        return expr_str
    
    
    async def handle_pair_command(app, msg, db, texts):
        seed(100*time.time() * msg.from_user.id)
        members = []
        async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.RECENT):
            if db.exists('users', 'id', m.user.id):
                members.append(m.user.id)

        member_1 = choice(members)
        member_2 = choice(members)
        
        user_1 = db.find_by_column('users', 'id', member_1)
        user_2 = db.find_by_column('users', 'id', member_2)
        
        if not user_1 or not user_2:
            main.check_user_id(db, member_1)
            main.check_user_id(db, member_2)
            user_1 = db.find_by_column('users', 'id', member_1)
            user_2 = db.find_by_column('users', 'id', member_2)
            
        name_1 = main.get_user_name(user_1[0])
        name_2 = main.get_user_name(user_2[0])
        await app.send_sticker(
            chat_id=msg.chat.id,  # ID чата, куда отправляем стикер
            sticker=texts.stickers['love'],
            protect_content=True
        )
        await msg.reply_text(texts.msg_pairing(name_1, name_2))

    async def handle_chance_command(app, msg, text, db):
        seed(100*time.time() * msg.from_user.id)
        percent = randint(10, 1000)/10
        user = db.find_by_column('users', 'id', msg.from_user.id)[0]
        name = main.get_user_name(user)
        phrase = choice(texts.phrases)
        res = f"{name}, {phrase} вероятность {percent}%"
        await msg.reply_text(res)

    async def handle_yes_no_command(app, msg, text, db):
        seed(100*time.time() * msg.from_user.id)
        user = db.find_by_column('users', 'id', msg.from_user.id)[0]
        name = main.get_user_name(user)
        phrase = choice(texts.predictions)
        res = f"{name}, {phrase}"
        await msg.reply_text(res)

    # Функция для сбора сообщений за указанный период
    async def collect_messages(app, chat_id, start_time):
        messages = []
        async for message in app.search_messages(chat_id, limit=10000, offset_date=start_time):
            messages.append(message)
        return messages

    # Функция для подсчета количества сообщений каждого пользователя
    def analyze_messages(messages):
        user_message_count = {}
        for message in messages:
            user_id = message.from_user.id if message.from_user else None
            if user_id:
                if user_id in user_message_count:
                    user_message_count[user_id] += 1
                else:
                    user_message_count[user_id] = 1
        return user_message_count

    # Функция для преобразования пользовательского ID в имя
    async def get_usernames(user_message_count, app):
        user_names = {}
        for user_id in user_message_count:
            user = await app.get_users(user_id)
            user_names[user_id] = user.first_name or user.username or str(user_id)
        return user_names

    # Функция для получения топ N пользователей
    async def get_top_users(app, chat_id, start_time, top_n=10):
        messages = await main.collect_messages(app, chat_id, start_time)
        user_message_count = main.analyze_messages(messages)
        user_names = await main.get_usernames(user_message_count, app)
        
        sorted_users = sorted(user_message_count.items(), key=lambda x: x[1], reverse=True)
        top_users = [(user_names[user_id], count) for user_id, count in sorted_users[:top_n]]
        total_messages = sum(user_message_count.values())
        return top_users, total_messages

    def create_roulette_video(names: list, output_file='temp.mp4', width=600, height=600, cell_height=150, 
                            rotation_speed=14000, duration=6, freeze_duration=4, fps=60):
        # Параметры
        n_cells = height // cell_height + 2
        if len(names) < n_cells:
            # Расширяем names до n_cells с помощью случайного выбора
            while len(names) < n_cells:
                names.append(choice(names))  # Добавляем случайный элемент из names

        shuffle(names)
        colors = [tuple(randint(0, 255) for _ in range(3)) for _ in range(n_cells)]

        # Функция для создания кадра
        def create_frame(position):
            frame = Image.new('RGB', (width, height), (0, 0, 0))
            draw = ImageDraw.Draw(frame)
            font = ImageFont.truetype('source/roulette_font.ttf', 64)  # Путь к вашему шрифту

            for i in range(n_cells):
                y = (position + i * cell_height) % (height + cell_height) - cell_height
                if 0 <= y < height:
                    # Рисуем ячейку
                    draw.rectangle([0, int(y), width, int(y + cell_height)], fill=colors[i])
                    # Определяем размеры и положение текста
                    text = names[i]
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
                    text_x = (width - text_width) // 2
                    text_y = int(y + cell_height / 2 - text_height / 2)
                    # Рисуем текст по центру ячейки
                    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

            # Добавляем белую полоску по середине экрана
            middle_y = height // 2
            draw.line((0, middle_y, width, middle_y), fill=(255, 0, 255), width=1)
            
            return np.array(frame)

        # Настройки анимации
        total_frames = duration * fps
        freeze_frames = freeze_duration * fps

        # Создание видео
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Генерация кадров
        for frame_number in range(total_frames):
            position = frame_number * rotation_speed / total_frames
            frame = create_frame(position)
            video_writer.write(frame)

        # Генерация кадров для показа последнего состояния
        last_frame = create_frame(position)
        for _ in range(freeze_frames):
            video_writer.write(last_frame)

        # Завершение записи видео
        video_writer.release()
        cv2.destroyAllWindows()

        return output_file


    async def rp_command(app, msg, texts, db):
        user = db.find_by_column('users', 'id', msg.from_user.id)
        if user:
            user = user[0]
            rp_commands = ast.literal_eval(user['rp'])
            verb = rp_commands.get(msg.text[1:-1])
            if verb:
                print(verb)
            elif texts.check_rp(msg.text[1:-1]):
                user1 = db.find_by_column('users', 'id', msg.from_user.id)
                user2 = db.find_by_column('users', 'id', msg.reply_to_message.from_user.id)  # Убедитесь, что второй пользователь правильный

                if user1 and user2:
                    user1 = user1[0]
                    user2 = user2[0]

                    gender1, gender2 = user1['gender'], user2['gender']

                    match1 = re.search(r'\((.*?)\)', user1['gender'])
                    match2 = re.search(r'\((.*?)\)', user2['gender'])

                    gender1 = match1.group(1)
                    gender2 = match2.group(1)

                    name1 = main.get_user_name(user1)
                    name2 = main.get_user_name(user2)

                    if gender1 == gender2:
                        gender = 'neutral'
                    elif gender1 == 'М':
                        gender = 'male'
                    elif gender1 == 'Д':
                        gender = 'female'

                    result = texts.get_rp(msg.text[1:-1])
                    reply_text = f"{texts.get_random_emoji()} | {texts.refactor_rp(result, name1, name2, gender)}"
                    await msg.reply_text(reply_text)
            else:
                await msg.reply_text('Такой команды у вас не создано(\n РП команды можно создать в лс')

    def check_gender(text):
        gender_text = text.lower()
        
        male_variations = [
            "мужской", "мужчина", "муж", "он", "мужского", "мужское", "мужчины"
        ]
        female_variations = [
            "женский", "женщина", "жен", "она", "женского", "женское", "женщины"
        ]

        if any(variation in gender_text for variation in male_variations):
            return "М"
        elif any(variation in gender_text for variation in female_variations):
            return "Д"
        else:
            return None  # Если гендер не распознан
        
    def parse_sovm(url):
        # Получаем HTML-код страницы
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим таблицу с классом results
        table = soup.find('table', class_='results')

        # Словарь для хранения данных
        data_list = []

        # Переменные для хранения текущих данных
        current_title = None
        current_annotation = None
        current_results = []

        # Итерируем по всем строкам таблицы
        for tr in table.find_all('tr'):
            title_div = tr.find('div', class_='sign_annotation_title')
            
            if title_div:  # Если нашли новый заголовок
                # Если уже есть собранные данные, сохраняем их в список
                if current_title is not None:
                    data_list.append({
                        'title': current_title,
                        'annotation': current_annotation,
                        'results': current_results
                    })
                
                # Сбрасываем текущие данные
                current_title = title_div.get_text(strip=True)
                current_annotation = tr.find('div', class_='sign_annotation').get_text(strip=True) if tr.find('div', class_='sign_annotation') else None
                current_results = []  # Сброс списка результатов
            
            # Добавляем результаты, если они есть
            result_divs = tr.find_all('div', class_='result_one')
            for result_div in result_divs:
                current_results.append(result_div.get_text(strip=True))

        # Сохраняем последние собранные данные, если они есть
        if current_title is not None:
            data_list.append({
                'title': current_title,
                'annotation': current_annotation,
                'results': current_results
            })

        return choice(data_list)

    async def sovms(man_birthdate, woman_birthdate):
        url = f'https://misterius.ru/viewpage.php?page_id=3&date_man={man_birthdate}&date_woman={woman_birthdate}'
        result = main.parse_sovm(url)
        return choice(result['results'])