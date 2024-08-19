import logging
import re
import inspect

# Функция для удаления ANSI кодов
def remove_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Настраиваем логгер
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler("aicy.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Создаем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Настраиваем формат логов
formatter = logging.Formatter('%(asctime)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

async def log_bot(msg):
    # Determine the message type
    if msg.photo:
        msg_type = "PHOTO"
    elif msg.video:
        msg_type = "VIDEO"
    elif msg.sticker:
        msg_type = "STICKER"
    elif msg.voice:
        msg_type = "VOICE"
    elif msg.contact:
        msg_type = "CONTACT"
    else:
        msg_type = msg.text.replace('\n', ';') if msg.text else "NOT MSG"

    # Create the log message
    if msg.chat.id < 0:
        log_msg = (
            f"|text: {msg_type}"
            f"|id: {msg.from_user.id}"
            f"|name: {msg.from_user.first_name}:{msg.from_user.last_name}:{msg.from_user.username}"
            f"|chat_ID: {msg.chat.id}"
            f"|type: GROUP"
            f"|title: {msg.chat.title}"
        )
    else:
        log_msg = (
            f"|text: {msg_type}"
            f"|id: {msg.from_user.id}"
            f"|name: {msg.from_user.first_name}:{msg.from_user.last_name}:{msg.from_user.username}"
            f"|type: PRIVATE"
        )

    # Log the message with the function name and line number
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back
    caller_line = caller_frame.f_lineno
    caller_function_name = caller_frame.f_code.co_name

    logger.info(f"{caller_function_name}:{caller_line} {log_msg}")


def log_start():
    logger.error('Bot starts')

def log_warn(text: str):
    logger.warning(text)