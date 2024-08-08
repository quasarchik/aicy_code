import requests
from bs4 import BeautifulSoup

# URL сайта, который нужно парсить
url = 'https://misterius.ru/viewpage.php?page_id=3&date_man=16.5.2006&date_woman=17.12.2007'

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

    print(len(data_list))
