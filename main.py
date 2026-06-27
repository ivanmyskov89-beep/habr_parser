"""
Домашнее задание к лекции 6. «Web-scrapping»
Парсинг свежих статей с Хабра по ключевым словам
Поиск по всей доступной preview-информации (заголовок, preview, хабы, теги, автор)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ============================================================
# НАСТРОЙКИ
# ============================================================

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'алгоритм', 'аналитика']
URL = 'https://habr.com/ru/all/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# ============================================================
# ФУНКЦИИ
# ============================================================

def fetch_articles(url):
    """
    Получает список статей со страницы Хабра.
    Собирает все текстовые поля карточки для поиска:
    - заголовок
    - preview-текст
    - хабы (теги)
    - автор
    - компания
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    for article in soup.find_all('article'):
        # --- Заголовок и ссылка ---
        title_tag = article.find('h2')
        if not title_tag:
            continue
        
        link_tag = title_tag.find('a')
        if not link_tag:
            continue
        
        title = link_tag.text.strip()
        link = link_tag.get('href')
        if not link.startswith('http'):
            link = 'https://habr.com' + link
        
        # --- Дата ---
        time_tag = article.find('time')
        date = time_tag.get('datetime') if time_tag else None
        
        # --- Preview-текст ---
        preview_tag = article.find('div', class_='article-formatted-body')
        if not preview_tag:
            preview_tag = article.find('div', class_='tm-article-snippet__body')
        preview = preview_tag.text.strip() if preview_tag else ''
        
        # --- Хабы (теги) ---
        hubs = []
        hub_tags = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        if not hub_tags:
            # Альтернативный класс для хабов
            hub_tags = article.find_all('a', class_='hub-link')
        for tag in hub_tags:
            hubs.append(tag.text.strip())
        
        # --- Автор ---
        author_tag = article.find('a', class_='tm-user-info__username')
        if not author_tag:
            author_tag = article.find('a', class_='tm-article-snippet__author')
        author = author_tag.text.strip() if author_tag else ''
        
        # --- Компания ---
        company_tag = article.find('a', class_='tm-user-info__company')
        company = company_tag.text.strip() if company_tag else ''
        
        # --- Собираем весь текст для поиска ---
        full_text = f"{title} {preview} {' '.join(hubs)} {author} {company}".lower()
        
        articles.append({
            'title': title,
            'link': link,
            'date': date,
            'preview': preview,
            'hubs': hubs,
            'author': author,
            'company': company,
            'full_text': full_text
        })
    
    return articles


def check_keywords(text, keywords):
    """
    Проверяет, встречается ли хотя бы одно ключевое слово в тексте.
    Возвращает список найденных ключевых слов.
    """
    found = []
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return found


def main():
    """Главная функция"""
    print("=" * 60)
    print("ПАРСИНГ СВЕЖИХ СТАТЕЙ С ХАБРА")
    print(f"Ключевые слова: {', '.join(KEYWORDS)}")
    print("=" * 60)
    
    try:
        articles = fetch_articles(URL)
        print(f"Найдено статей: {len(articles)}")
        print("-" * 60)
        
        found_articles = []
        
        for article in articles:
            # Используем полный текст карточки (включая хабы, теги, автора)
            found_keywords = check_keywords(article['full_text'], KEYWORDS)
            
            if found_keywords:
                # Форматируем дату
                if article['date']:
                    try:
                        date_obj = datetime.fromisoformat(article['date'].replace('Z', '+00:00'))
                        date_str = date_obj.strftime('%d.%m.%Y')
                    except ValueError:
                        date_str = 'Дата неизвестна'
                else:
                    date_str = 'Дата неизвестна'
                
                found_articles.append({
                    'date': date_str,
                    'title': article['title'],
                    'link': article['link'],
                    'keywords': found_keywords,
                    'hubs': article.get('hubs', [])
                })
        
        # Вывод результатов
        if found_articles:
            print(f"\nНайдено {len(found_articles)} подходящих статей:\n")
            for item in found_articles:
                print(f"{item['date']} – {item['title']} – {item['link']}")
                if item['hubs']:
                    print(f"  Хабы: {', '.join(item['hubs'])}")
                print(f"  Ключевые слова: {', '.join(item['keywords'])}")
                print()
        else:
            print("\nСтатьи с указанными ключевыми словами не найдены.")
            
    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()