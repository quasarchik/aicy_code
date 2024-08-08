from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

class main:
    menu_kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton("Анкета🌸")],
                [KeyboardButton("Команды🍭"), KeyboardButton("Разработчик🏵")],
                [KeyboardButton("РП-команды✨")],
                [KeyboardButton("Ивенты🌑"), KeyboardButton("Хаб бота🌕")],
                [KeyboardButton("Баланс🌻")],
                
            ],
            resize_keyboard=True
        )