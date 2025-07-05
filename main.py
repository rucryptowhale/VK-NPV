import os
import requests
from datetime import datetime

# Конфигурация
GROUP_ID = "netpresentvalue"  # Используем короткое имя сообщества
VK_API_KEY = os.environ["VK_API_KEY"]
VK_API_VERSION = "5.199"

def get_group_stats():
    """Получение статистики сообщества за последний день"""
    url = "https://api.vk.com/method/stats.get"
    params = {
        "group_id": GROUP_ID,
        "interval": "day",
        "access_token": VK_API_KEY,
        "v": VK_API_VERSION
    }
    try:
        response = requests.get(url, params=params).json()
        if 'error' in response:
            print(f"Ошибка VK API: {response['error']['error_msg']}")
            return {}
        return response.get("response", [{}])[-1] if response.get("response") else {}
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
    
    # Форматирование описания (удаляем лишние теги)
    description = info.get('description', 'Нет описания')
    description = description.replace('<br>', '\n').replace('&quot;', '"')
    
    return f"""
# {info.get('name', 'Net Present Value')} - Статистика сообщества

![Аватар сообщества]({info.get('photo_200', '')})

**Описание**:  
{description}

**Категория**: {info.get('activity', 'Финансы и инвестиции')}

**Участники**: {info.get('members_count', 0):,}

**Сайт сообщества**: [vk.link/netpresentvalue](https://vk.link/netpresentvalue)

## Статистика на {update_time}

| Показатель   | Значение |
|--------------|----------|
| Охват        | {stats.get('reach', 'N/A')} |
| Посетители   | {stats.get('visitors', 'N/A')} |
| Просмотры    | {stats.get('views', 'N/A')} |
| Лайки        | {stats.get('likes', 'N/A')} |
| Репосты      | {stats.get('shares', 'N/A')} |
| Комментарии  | {stats.get('comments', 'N/A')} |

> Данные обновляются автоматически через GitHub Actions
"""

if __name__ == "__main__":
    # Получаем данные
    group_info = get_group_info()
    group_stats = get_group_stats()
    
    # Генерируем и сохраняем README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(group_info, group_stats))
    
    print("README успешно обновлен!")