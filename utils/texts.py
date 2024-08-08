import random


class texts:
    stickers = {
        "annoyed": "source/stickers/vkzizi/annoyed.webp",
        "ban": "source/stickers/vkzizi/ban.webp",
        "bang": "source/stickers/vkzizi/bang.webp",
        "book": "source/stickers/vkzizi/book.webp",
        "broken": "source/stickers/vkzizi/broken.webp",
        "chill": "source/stickers/vkzizi/chill.webp",
        "clown": "source/stickers/vkzizi/clown.webp",
        "coctail": "source/stickers/vkzizi/coctail.webp",
        "cringe": "source/stickers/vkzizi/cringe.webp",
        "cry": "source/stickers/vkzizi/cry.webp",
        "cutie": "source/stickers/vkzizi/cutie.webp",
        "dance": "source/stickers/vkzizi/dance.webp",
        "depression": "source/stickers/vkzizi/depression.webp",
        "doll": "source/stickers/vkzizi/doll.webp",
        "faster": "source/stickers/vkzizi/faster.webp",
        "fear": "source/stickers/vkzizi/fear.webp",
        "genius": "source/stickers/vkzizi/genius.webp",
        "getout": "source/stickers/vkzizi/getout.webp",
        "good": "source/stickers/vkzizi/good.webp",
        "infire": "source/stickers/vkzizi/infire.webp",
        "inhouse": "source/stickers/vkzizi/inhouse.webp",
        "love": "source/stickers/vkzizi/love.webp",
        "lowbattery": "source/stickers/vkzizi/lowbattery.webp",
        "marryme": "source/stickers/vkzizi/marryme.webp",
        "mm": "source/stickers/vkzizi/mm.webp",
        "music": "source/stickers/vkzizi/music.webp",
        "no": "source/stickers/vkzizi/no.webp",
        "notebook": "source/stickers/vkzizi/notebook.webp",
        "nothing": "source/stickers/vkzizi/nothing.webp",
        "one": "source/stickers/vkzizi/one.webp",
        "pain": "source/stickers/vkzizi/pain.webp",
        "plaid": "source/stickers/vkzizi/plaid.webp",
        "popcorn": "source/stickers/vkzizi/popcorn.webp",
        "reverse": "source/stickers/vkzizi/reverse.webp",
        "sleep": "source/stickers/vkzizi/sleep.webp",
        "sleeping": "source/stickers/vkzizi/sleeping.webp",
        "socutie": "source/stickers/vkzizi/socutie.webp",
        "sorry": "source/stickers/vkzizi/sorry.webp",
        "study": "source/stickers/vkzizi/study.webp",
        "tea": "source/stickers/vkzizi/tea.webp",
        "thinking": "source/stickers/vkzizi/thinking.webp",
        "time": "source/stickers/vkzizi/time.webp",
        "understand": "source/stickers/vkzizi/understand.webp",
        "uy": "source/stickers/vkzizi/uy.webp",
        "what": "source/stickers/vkzizi/what.webp",
        "wow": "source/stickers/vkzizi/wow.webp",
        "xexexe": "source/stickers/vkzizi/xexexe.webp",
        "yes": "source/stickers/vkzizi/yes.webp"
    }

    greeting_private = '''
    Привет! 😊 Я — ваш личный помощник AICY. 
    Как я могу помочь вам сегодня? 
    Если у вас есть вопросы или задачи, не стесняйтесь обращаться! 🚀
    '''

    greeting_group = '''
    Привет, команда! 🎉 Я — AICY, ваш универсальный бот. 
    Рад быть с вами! Если нужна помощь или есть вопросы, не стесняйтесь обращаться. 
    Вперед к новым достижениям! 🌟
    '''

    random_love_emoji = lambda: random.choice("❤️ 💕 💖 💗 💓 💞 💘 💌 💝 💟 💙 💚 💛 🧡 💜 🥰 😍 😘 🤗 💑 💏".split(' '))
    emojis = [
        "😊", "😂", "😢", "😍", "😎", "🤔", "😱", "😴", "🤗", "🥳",
        "🤖", "👻", "🌟", "✨", "🔥", "💧", "🍀", "🌈", "🍕", "🌮",
        "⚔️", "🛡️", "🏰", "🧙‍♂️", "🧚", "🐉", "🦄", "🐾", "🌊", "🌍",
        "🌌", "🏹", "⛷️", "🚀", "🎭", "🎨", "🎉", "🎵", "🎮", "🧩"
    ]
    get_random_emoji = lambda: random.choice(texts.emojis)
    phrases = (
        "🤔 Я думаю, что",
        "☝ Я уверен, что",
        "🤷 Я не уверен, но",
        "🧐 Мне кажется, что",
        "💡 Я считаю, что",
        "🔍 На мой взгляд,",
        "📈 По моему мнению,",
        "🚀 Я предполагаю, что",
        "🤔 Возможно, что",
        "🌟 Я предполагаю, что"
    )
    predictions = (
        "✨ Конечно, все предрешено!",
        "🤔 Ой, не знаю, попробуй еще разик!",
        "🌟 Все звезды говорят 'да'!",
        "💫 Хм, похоже что нет",
        "🎀 Уверена, что да!",
        "💖 Ммм, все-таки это может быть нет.",
        "🌈 Вероятно, что 'да', но вселенная все еще раздумывает.",
        "🧸 Увы, но на этот раз 'нет', не грусти!",
        "🌹 О, да, счастье на твоей стороне!",
        "🍀 Скорее 'да', но иногда звезды бывают капризными!"
    )
    # Messages for various actions with cooldown in hours

    shippers = [
        "💞 РАНДОМ ШИППЕРИМ",
        "💖 СЛУЧАЙНЫЙ ШИППЕР",
        "💘 ШИППЕРИМ С УДОВОЛЬСТВИЕМ",
        "💓 РАНДОМНЫЙ ШИП",
    ]

    love_phrases = [
        "Любите друг друга и берегите.",
        "Цените каждое мгновение вместе.",
        "Будьте счастливы вместе!",
        "С любовью, к лучшему!",
    ]

    mur_cats = [
        "Мур!",
        "Мяу!",
        "Мав!",
        "Мию!",
        "Мур-р-р!"
    ]

    # Функция для генерации сообщения
    def msg_pairing(name_1, name_2):
        shipper = random.choice(texts.shippers)
        love_phrase = random.choice(texts.love_phrases)
        cat = random.choice(texts.mur_cats)
        return f"{shipper}: {name_1} и {name_2}. {love_phrase} {cat}"
    
    invalid_get_my_data = "Такой информации нету, возможные значения - др, город, ник"

    get_my_data_nick = lambda name, nick: f"{name}, ваш ник {nick}"
    get_my_data_gender = lambda name, gender: f"{name}, ваш пол {gender}"
    get_my_data_city = lambda name, city: f"{name}, ваш город {city}"
    get_my_data_dr =  lambda name, birthdate, age, zodiac: f"{name}, ваш день рождения {birthdate} ({age} лет, {zodiac})"
    

    msg_pairing_not_get = lambda name, seconds: f"{name}📝 Лимит на вызов данной команды исчерпан\n⏱ Ограничение будет снято через {seconds} сек!\n👥 Ограничение на одного мурку"

    msg_already_played = lambda name, length, days, hours, minutes, seconds: f"{name}, ты уже играл.\nСейчас он равен {length} см.\nСледующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"
    msg_grew = lambda name, added, new_length: f"{name}, твой писюн вырос на {added} см.\nТеперь он равен {new_length} см.\nСледующая попытка через 24 часа!"
    msg_shrank = lambda name, added, new_length: f"{name}, твой писюн уменьшился на {-added} см.\nТеперь он равен {new_length} см.\nСледующая попытка через 24 часа!"

    msg_already_had_beer = lambda name, count, days, hours, minutes, seconds: f"{name}, ты уже пил пиво сегодня.\nСейчас в тебе {count} кружек пива.\nСледующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"
    msg_drunk_beer = lambda name, added, new_count: f"{name}, ты выпил {added} кружек пива.\nТеперь в тебе {new_count} кружек пива.\nСледующая попытка через 24 часа!"

    msg_already_had_kymyz = lambda name, count, days, hours, minutes, seconds: f"{name}, ты уже пил кымыз сегодня.\nСейчас в тебе {count} чашек кымыза.\nСледующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"
    msg_drunk_kymyz = lambda name, added, new_count: f"{name}, ты выпил {added} чашек кымыза.\nТеперь в тебе {new_count} чашек кымыза.\nСледующая попытка через 24 часа!"

    msg_already_had_coffee = lambda name, count, days, hours, minutes, seconds: f"{name}, ты уже пил кофе сегодня.\nСейчас в тебе {count} кружек кофе.\nСледующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"
    msg_drunk_coffee = lambda name, added, new_count: f"{name}, ты выпил {added} кружек кофе.\nТеперь в тебе {new_count} кружек кофе.\nСледующая попытка через 24 часа!"

    msg_already_had_tea = lambda name, count, days, hours, minutes, seconds: f"{name}, ты уже пил чай сегодня.\nСейчас в тебе {count} кружек чая.\nСледующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"
    msg_drunk_tea = lambda name, added, new_count: f"{name}, ты выпил {added} кружек чая.\nТеперь в тебе {new_count} кружек чая.\nСледующая попытка через 24 часа!"

    msg_farm_coins = lambda name, added, added_coins: f"{name}, 💜 АЙС! 💜\n +{added} ₳ в мешок"
    msg_already_farm_coins = lambda name, coins, days, hours, minutes, seconds: f"{name},\n💢 НОТАЙС! 💢 Фармить можно раз в день! Следующая попытка через {days} дн. {hours} ч. {minutes} мин. {seconds} сек!"


    msg_nickname_saved = lambda nickname: f"✨ Ваш новый никнейм: {nickname} \n✅ Успешно сохранён!"
    msg_nickname_deleted = "🗑️ Ваш никнейм был успешно удалён!"
    msg_nickname_invalid = lambda nickname: f"🚫 Никнейм '{nickname}' содержит запрещённые символы!"

    msg_gender_saved = lambda nickname: f"✨ Ваш пол: {nickname} \n✅ Успешно сохранён!"
    msg_gender_deleted = "🗑️ Ваш пол был успешно удалён!"
    msg_gender_invalid = lambda nickname: f"🚫 Пол '{nickname}' не разпознан!"

    msg_city_saved = lambda nickname: f"✨ Ваш город: {nickname} \n✅ Успешно сохранён!"
    msg_city_deleted = "🗑️ Ваш город был успешно удалён!"
    msg_city_invalid = lambda nickname: f"🚫 Город '{nickname}' содержит запрещённые символы!"
    
    # Пример обновленного текста
    msg_birthdate_saved = lambda age, zodiac: f"Ваша дата рождения сохранена!\nВаш возраст: {age}!\nВаш знак зодиака: {zodiac}!"
    msg_birthdate_deleted = "🗑️ Ваша дата рождения была успешно удалена!"
    msg_birthdate_invalid = "❌ Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ 📅"


    def get_info_chat(msg):
        user_id = msg.from_user.id
        user_name = msg.from_user.username
        chat_id = msg.chat.id
        reply_user_id = msg.reply_to_message.from_user.id if msg.reply_to_message else None
        reply_user_name = msg.reply_to_message.from_user.username if msg.reply_to_message else None

        info_text = (
            f"User ID: {user_id}\n"
            f"Username: @{user_name}\n"
            f"Chat ID: {chat_id}\n"
        )

        if reply_user_id:
            info_text += (
                f"Reply User ID: {reply_user_id}\n"
                f"Reply Username: @{reply_user_name}\n"
            )
        return info_text
        
    def load_commands(file_path):
        commands = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                # Разделяем строку на команду и текст
                command, text = line.split(' | ')
                commands[command] = text
        return commands
    commands = load_commands('utils/standard_rp.txt')
    
    def check_rp(verb):
        for command in texts.commands.keys():
            if verb == command:
                return True
        return False


    def get_rp(verb):
        res = ''
        for command in texts.commands.keys():
            if verb == command:
                res = texts.commands[command]
        return res

    def refactor_rp(res, name1, name2, gender):
        # Заменяем @u1 и @u2 на name1 и name2
        res = res.replace('@u1', name1).replace('@u2', name2)
        
        return res
        