from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Инициализация модели и токенизатора
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Инициализация переменной для хранения истории сообщений
chat_history_ids = None

print("🤖 Привет! Я чат-бот. Напиши мне что-нибудь, и я постараюсь ответить! (введите 'выход' для завершения)")

# Основной цикл взаимодействия с пользователем
while True:
    user_input = input("Вы: ")

    # Проверка на команду выхода
    if user_input.lower() == 'выход':
        print("🤖 До свидания!")
        break

    # Токенизация пользовательского ввода и создание input_ids
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Объединяем новый ввод с историей сообщений
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        input_ids = new_input_ids

    # Генерация ответа
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Получение текста ответа
    bot_reply = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=False)

    print(f"🤖 Бот: {bot_reply}")
