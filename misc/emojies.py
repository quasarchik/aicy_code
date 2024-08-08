import random

def get_random_emoji(theme):
    emojis = {
        'happy': ['😊', '😃', '😁', '😄', '😆'],
        'sad': ['😢', '😔', '😞', '😩', '😭'],
        'love': ['❤️', '😍', '😘', '💕', '💖'],
        'angry': ['😠', '😡', '🤬', '😤', '😒'],
        'surprised': ['😲', '😮', '😯', '😳', '🤯'],
        'food': ['🍎', '🍔', '🍕', '🍣', '🍦'],
        'animals': ['🐶', '🐱', '🐻', '🐨', '🐼'],
        'sports': ['⚽', '🏀', '🏈', '🎾', '🏓']
    }
    
    if theme in emojis:
        return random.choice(emojis[theme])
    else:
        return '🤔'  # Возвращаем эмоджи "думающий", если тема не найдена

# Примеры использования
print(get_random_emoji('happy'))  # Вывод: 😃 (или другая случайная эмоджи)
print(get_random_emoji('food'))   # Вывод: 🍕 (или другая случайная эмоджи)
print(get_random_emoji('unknown'))  # Вывод: 🤔
