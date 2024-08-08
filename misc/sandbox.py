import logging
import re

# Функция для удаления ANSI кодов
def remove_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Настраиваем логгер
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler("cleaned_file.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Создаем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Настраиваем формат логов
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Пример использования
logger.info(remove_ansi_codes("This is an info message"))