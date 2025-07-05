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

def generate_analytics_svg(stats):
    """Генерация SVG графика статистики"""
    # Вычисляем максимальное значение для масштабирования
    max_val = max(
        stats.get('reach', 0),
        stats.get('visitors', 0),
        stats.get('views', 0),
        max(1, stats.get('likes', 0) * 5),  # Увеличиваем для видимости
        max(1, stats.get('shares', 0) * 10),
        max(1, stats.get('comments', 0) * 10)
    ) or 1
    
    scale = 150 / max_val  # Высота графика 150px
    
    svg_content = f"""<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
        <style>
            .bar {{ 
                fill: #58a6ff; 
                transition: height 0.5s;
            }}
            .bar:hover {{ 
                fill: #1f6feb; 
                filter: url(#glow);
            }}
            .label {{ 
                font: 12px sans-serif; 
                fill: #c9d1d9; 
            }}
            .title {{ 
                font: 16px sans-serif; 
                fill: #58a6ff; 
                font-weight: bold; 
            }}
            .axis {{ 
                stroke: #30363d; 
                stroke-width: 1; 
            }}
            .grid {{ 
                stroke: #30363d; 
                stroke-width: 0.5;
                stroke-dasharray: 2,2;
            }}
            .value {{ 
                font: 10px sans-serif; 
                fill: #8b949e; 
                text-anchor: middle;
            }}
        </style>
        
        <!-- Эффект свечения при наведении -->
        <defs>
            <filter id="glow" height="300%" width="300%" x="-75%" y="-75%">
                <feGaussianBlur stdDeviation="2.5" result="blurred"/>
                <feMerge>
                    <feMergeNode in="blurred"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        
        <rect width="100%" height="100%" fill="#0d1117" />
        
        <!-- Заголовок -->
        <text x="300" y="30" text-anchor="middle" class="title">📊 Статистика сообщества</text>
        
        <!-- Сетка и оси -->
        <line x1="50" y1="50" x2="50" y2="200" class="axis" />
        <line x1="50" y1="200" x2="550" y2="200" class="axis" />
        
        <!-- Горизонтальные линии сетки -->
        <line x1="50" y1="150" x2="550" y2="150" class="grid" />
        <line x1="50" y1="100" x2="550" y2="100" class="grid" />
        <line x1="50" y1="50" x2="550" y2="50" class="grid" />
        
        <!-- Подписи осей -->
        <text x="30" y="125" text-anchor="middle" transform="rotate(-90,30,125)" class="label">Значение</text>
        <text x="300" y="230" text-anchor="middle" class="label">Показатели</text>
        
        <!-- Бар-чарт -->
        <g transform="translate(0, 0)">
            <!-- Охват -->
            <rect class="bar" x="70" y="{200 - stats.get('reach', 0)*scale}" width="40" height="{stats.get('reach', 0)*scale}" />
            <text class="value" x="90" y="{195 - stats.get('reach', 0)*scale}">{stats.get('reach', 0)}</text>
            <text class="label" x="90" y="220" text-anchor="middle">Охват</text>
            
            <!-- Посетители -->
            <rect class="bar" x="150" y="{200 - stats.get('visitors', 0)*scale}" width="40" height="{stats.get('visitors', 0)*scale}" />
            <text class="value" x="170" y="{195 - stats.get('visitors', 0)*scale}">{stats.get('visitors', 0)}</text>
            <text class="label" x="170" y="220" text-anchor="middle">Посетители</text>
            
            <!-- Просмотры -->
            <rect class="bar" x="230" y="{200 - stats.get('views', 0)*scale}" width="40" height="{stats.get('views', 0)*scale}" />
            <text class="value" x="250" y="{195 - stats.get('views', 0)*scale}">{stats.get('views', 0)}</text>
            <text class="label" x="250" y="220" text-anchor="middle">Просмотры</text>
            
            <!-- Лайки -->
            <rect class="bar" x="310" y="{200 - stats.get('likes', 0)*scale*5}" width="40" height="{stats.get('likes', 0)*scale*5}" />
            <text class="value" x="330" y="{195 - stats.get('likes', 0)*scale*5}">{stats.get('likes', 0)}</text>
            <text class="label" x="330" y="220" text-anchor="middle">Лайки</text>
            
            <!-- Репосты -->
            <rect class="bar" x="390" y="{200 - stats.get('shares', 0)*scale*10}" width="40" height="{stats.get('shares', 0)*scale*10}" />
            <text class="value" x="410" y="{195 - stats.get('shares', 0)*scale*10}">{stats.get('shares', 0)}</text>
            <text class="label" x="410" y="220" text-anchor="middle">Репосты</text>
            
            <!-- Комментарии -->
            <rect class="bar" x="470" y="{200 - stats.get('comments', 0)*scale*10}" width="40" height="{stats.get('comments', 0)*scale*10}" />
            <text class="value" x="490" y="{195 - stats.get('comments', 0)*scale*10}">{stats.get('comments', 0)}</text>
            <text class="label" x="490" y="220" text-anchor="middle">Комментарии</text>
        </g>
    </svg>"""
    
    with open("analytics.svg", "w") as f:
        f.write(svg_content)

def generate_readme(info, stats):
    """Генерация README.md с профессиональным дизайном"""
    update_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    # Форматирование описания
    description = info.get('description', 'Нет описания')
    description = description.replace('<br>', '\n').replace('&quot;', '"')
    
    # Форматирование числа участников
    members_count = info.get('members_count', 0)
    formatted_members = f"{members_count:,}".replace(',', ' ')
    
    # SVG разделитель
    separator_svg = """
<svg width="100%" height="20" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="2" fill="#0d1117" />
  <rect y="18" width="100%" height="2" fill="#0d1117" />
  <path d="M0 10 Q 50 15, 100 10 T 200 10" stroke="#58a6ff" stroke-width="2" fill="none" />
</svg>
"""
    
    # Форматирование статистики
    def format_stat(value, label, color):
        return f"![{label}](https://img.shields.io/badge/{label.replace(' ', '_')}-{value}-{color}?style=flat-square&logo=github)"
    
    return f"""# 🚀 {info.get('name', 'Net Present Value')} - Профессиональная аналитика

{separator_svg}

<div align="center">
  <img src="{info.get('photo_200', '')}" alt="Логотип сообщества" width="200" style="border-radius: 10px; border: 2px solid #58a6ff;">
</div>

## 📌 Основная информация

> **Описание**:  
> {description}

| Характеристика      | Значение                          |
|---------------------|-----------------------------------|
| **🏷️ Категория**   | `{info.get('activity', 'Финансы и инвестиции')}` |
| **👥 Участники**    | `{formatted_members}`             |
| **🌐 Сайт**         | [vk.link/netpresentvalue](https://vk.link/netpresentvalue) |

{separator_svg}

## 📊 Статистика сообщества

<div align="center">
  <img src="analytics.svg" alt="График статистики" width="100%">
</div>

<div align="center" style="margin-top: 20px; margin-bottom: 20px;">

{format_stat(stats.get('reach', 0), 'Охват', 'blue')}
{format_stat(stats.get('visitors', 0), 'Посетители', 'orange')}
{format_stat(stats.get('views', 0), 'Просмотры', 'green')}

{format_stat(stats.get('likes', 0), 'Лайки', 'red')}
{format_stat(stats.get('shares', 0), 'Репосты', 'violet')}
{format_stat(stats.get('comments', 0), 'Комментарии', 'yellow')}

</div>

{separator_svg}

## ⚙️ Техническая информация

- **🔄 Последнее обновление**: {update_time}
- **📡 Источник данных**: VK API
- **🤖 Автоматизация**: GitHub Actions
- **⏱️ Частота обновления**: Ежедневно
- **💾 Репозиторий**: [rucryptowhale/VK-NPV](https://github.com/rucryptowhale/VK-NPV)

<div align="center" style="margin-top: 20px;">
  <a href="https://github.com/rucryptowhale/VK-NPV">
    <img src="https://img.shields.io/badge/GitHub-Repo-brightgreen?logo=github&style=for-the-badge" alt="GitHub Repo">
  </a>
  <a href="https://vk.com/netpresentvalue">
    <img src="https://img.shields.io/badge/VK-Сообщество-blue?logo=vk&style=for-the-badge" alt="VK Community">
  </a>
</div>

<div align="center" style="margin-top: 30px;">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=435&lines=Powered+by+GitHub+Actions;Professional+Analytics;Data+Driven+Decisions;Made+with+❤️+by+IT+specialists" alt="Typing SVG">
</div>
"""

if __name__ == "__main__":
    group_info = get_group_info()
    group_stats = get_group_stats()
    
    # Генерация графика
    generate_analytics_svg(group_stats)
    
    # Генерация README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(group_info, group_stats))
    
    print("README успешно обновлен!")
