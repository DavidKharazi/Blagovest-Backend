import sqlite3
import requests
from bs4 import BeautifulSoup

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect('parser.db')
cursor = conn.cursor()

# Создание таблицы, если она еще не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        image_url TEXT
    )
''')
conn.commit()

# Парсинг заголовков статей (https://www.mtsmonline.ru/resources/articles)
base_url = 'https://www.mtsmonline.ru/resources/articles#3189678-1'
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='article')

    for i, article in enumerate(articles):
        title = article.find('div', class_='title')
        title_text = title.text.strip() if title else 'Нет заголовка'

        print(f'Статья {i + 1} - Название: {title_text}\n{"=" * 50}')

        # Получение ссылки на статью
        article_url = article.find('a')['href'] if article.find('a') else None

        # Получение URL изображения
        image_url = article.find('img', class_='image-element')['src'] if article.find('img', class_='image-element') else 'your_default_image_url_here'

        if article_url:
            # Подключение к базе данных перед выполнением запроса INSERT
            conn = sqlite3.connect('parser.db')
            cursor = conn.cursor()

            # Парсинг содержимого статьи (https://www.russiaworship.ru/resources/articles/read/article/1702631)
            response_article = requests.get(article_url)

            if response_article.status_code == 200:
                soup_article = BeautifulSoup(response_article.text, 'html.parser')
                paragraphs = soup_article.find_all('p')

                content = '\n'.join([p.text for p in paragraphs])

                # Добавление данных в базу данных
                cursor.execute('''
                    INSERT INTO articles (title, content, image_url)
                    VALUES (?, ?, ?)
                ''', (title_text, content, image_url))

                conn.commit()

                print('=' * 50 + '\n')

                # Закрытие соединения с базой данных
                conn.close()
            else:
                print(f'Не удалось получить доступ к статье {article_url}. Код состояния:', response_article.status_code)
else:
    print(f'Не удалось получить доступ к странице {base_url}. Код состояния:', response.status_code)

# Закрытие соединения с базой данных (переместите этот блок в конец скрипта)
conn.close()




