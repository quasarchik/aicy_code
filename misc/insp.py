import inspect

def example_function():
    # Получаем текущий стек вызовов
    current_frame = inspect.currentframe()
    # Переходим на уровень выше в стеке вызовов
    caller_frame = current_frame.f_back
    # Получаем информацию о строке и файле
    caller_line = caller_frame.f_lineno
    caller_function_name = caller_frame.f_code.co_name
    
    print(f'Функция была вызвана из: {caller_function_name}, строка: {caller_line}')

def another_function():
    example_function()

# Пример вызова
another_function()