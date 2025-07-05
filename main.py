import os
import requests
from datetime import datetime, timedelta

# Конфигурация
GROUP_ID = "226396402"  # Используем числовой ID без "club"
VK_API_KEY = os.environ["VK_API_KEY"]
VK_API_VERSION = "5.199"

def get_group_stats():
    """Получение статистики сообщества за последний день"""
    url = "https://api.vk.com/method/stats.get"
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    params = {
        "group_id": GROUP_ID,
        "date_from": yesterday,
        "date_to": yesterday,
        "access_token": VK_API_KEY,
        "v": VK_API_VERSION
    }
    try:
        response = requests.get(url, params=params).json()
        if 'error' in response:
            print(f"Ошибка VK API: {response['error']['error_msg']}")
            return {}
        
        # Обработка случая, когда статистика еще не сформирована
        if not response.get('response') or not response['response']:
            print("Статистика за вчерашний день еще не доступна")
            return {
                'reach': 0,
                'visitors': 0,
                'views': 0,
                'likes': 0,
                'shares': 0,
                'comments': 0
            }
            
        return response['response'][0]
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        return {}

def get_group_info():
    """Получение основной информации о сообществе"""
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "group_ids": GROUP_ID,
        "fields": "name,description,members_count,photo_200,activity,site",
        "access_token": VK_API_KEY,
        "v": VK_API_VERSION
    }
    try:
        response = requests.get(url, params=params).json()
        if 'error' in response:
            print(f"Ошибка VK API: {response['error']['error_msg']}")
            return {}
        return response["response"][0] if response.get("response") else {}
    except Exception as e:
        print(f"Ошибка при получении информации о группе: {e}")
        return {}

def generate_readme(info, stats):
    """Генерация README.md с актуальными данными"""
    update_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    # Форматирование описания
    description = info.get('description', 'Нет описания')
    description = description.replace('<br>', '\n').replace('&quot;', '"')
    
    # Форматирование числа участников
    members_count = info.get('members_count', 0)
    formatted_members = f"{members_count:,}".replace(',', ' ')
    
    return f"""# {info.get('name', 'Net Present Value')} - Статистика сообщества

![Аватар сообщества]({info.get('photo_200', '')})

**Описание**:  
{description}

**Категория**: {info.get('activity', 'Финансы и инвестиции')}

**Участники**: {formatted_members}

**Сайт сообщества**: [vk.link/netpresentvalue](https://vk.link/netpresentvalue)

## Статистика на {update_time}

| Показатель   | Значение |
|--------------|----------|
| Охват        | {stats.get('reach', 0)} |
| Посетители   | {stats.get('visitors', 0)} |
| Просмотры    | {stats.get('views', 0)} |
| Лайки        | {stats.get('likes', 0)} |
| Репосты      | {stats.get('shares', 0)} |
| Комментарии  | {stats.get('comments', 0)} |

> Данные обновляются автоматически через GitHub Actions
"""

if __name__ == "__main__":
    group_info = get_group_info()
    group_stats = get_group_stats()
    
    # Генерация README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(group_info, group_stats))
    
    print("README успешно обновлен!")
