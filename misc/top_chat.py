import json
from datetime import datetime, timedelta

# Функция для загрузки данных всех пользователей из JSON файла
def load_data(filename='messages.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Функция для сохранения сообщения определенного пользователя в JSON файл
def save_message(user, text, filename='messages.json'):
    data = load_data(filename)
    if user not in data:
        data[user] = []
    # Сохраняем текущее время в формате строки "YYYY-MM-DD HH:MM:SS"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data[user].append({"text": text, "timestamp": current_time})
    with open(filename, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Функция для подсчета сообщений каждого пользователя за определённый период
def count_messages(time_period, filename='messages.json'):
    data = load_data(filename)
    now = datetime.now()

    if time_period == 'час':
        start_time = now - timedelta(hours=1)
    elif time_period == 'минуту':
        start_time = now - timedelta(minutes=1)
    elif time_period == 'день':
        start_time = now - timedelta(days=1)
    elif time_period == 'неделю':
        start_time = now - timedelta(weeks=1)
    elif time_period == 'месяц':
        start_time = now.replace(day=1)
    elif time_period == 'год':
        start_time = now.replace(month=1, day=1)
    else:
        print("Неизвестный период времени.")
        return

    for user, messages in data.items():
        count = sum(1 for message in messages if datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S') >= start_time)
        print(f"{user}: {count} сообщений за {time_period}")

# Пример использования
save_message("user1", "Пример сообщения от user1")
save_message("user2", "Пример сообщения от user2")
count_messages("час")
count_messages("день")
