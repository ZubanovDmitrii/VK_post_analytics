import requests
from datetime import datetime
import csv
import os

# Получение данных о постах со страницы пользователя ВК
def get_vk_posts_likes(access_token, domain = None, count = 100):
    base_url = "https://api.vk.com/method/wall.get"
    params = {
        'access_token': access_token,
        'v': '5.131',
        'count': count,
        'extended': 1
    }

    if domain:
        params['domain'] = domain
    else:
        raise ValueError("Необходимо указать domain")

    try:
        response = requests.get(base_url, params = params)
        data = response.json()

        # Проверка наличия ошибок
        if 'error' in data:
            print(f"Ошибка VK API: {data['error']['error_msg']}")
            return []

        # Извлечение полученных данных
        posts_data = []
        posts = data['response']['items']

        for post in posts:
            # Пропуск репостов
            if 'copy_history' in post:
                continue

            post_date = datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')
            likes_count = post['likes']['count'] if 'likes' in post else 0

            posts_data.append({
                'date': post_date,
                'likes': likes_count,
                'post_id': post['id']
            })
        return posts_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

# Сохранение полученных данных о постах в CSV файл
def save_to_csv(posts_data, filename = None):
    # Проверка наличия данных для сохранения
    if not posts_data:
        print("Нет данных для сохранения")
        return False
    # Генерация имени файла, если не указано
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vk.posts_analysis_{timestamp}.csv"

    try:
        # Сортировка по дате (от новых к старым)
        posts_data.sort(key=lambda x: x['date'], reverse = True)

        # Определение полей CSV
        fieldnames = ['post_id', 'date', 'likes']

        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Запись заголовка
            writer.writeheader()
            # Запись данных
            for post in posts_data:
                writer.writerow(post)

        print(f"Данные успешно сохранены в файл: {filename}")
        print(f"Всего сохранено записей: {len(posts_data)}")

        return True

    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")
        return False

def main():
    # Токен доступа VK API (ввести свой)
    access_token = "access_token"
    # Короткое имя пользователя ВК
    domain = 'dm'
    # Количество постов для получения (максимум 100)
    posts_count = 100
    # Имя файла для сохранения
    csv_filename = 'posts.csv'

    # Получение данных о постах
    print ("Получение данных из VK...")
    posts_data = get_vk_posts_likes(
        access_token = access_token,
        domain = domain,
        count = posts_count
    )
    # Сохранение полученных данных о постах
    if posts_data:
        save_to_csv(posts_data, csv_filename)
        print(f"\nФайлы успешно созданы:")
        print(f"- {csv_filename} - основные данные о постах")
    else:
        print("Не удалось получить данные или посты отсутствуют")

if __name__ == "__main__":
    main()