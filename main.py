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
  <img src="{info.get('photo_200', '')}" alt="Логотип сообщества" width="200">
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

{format_stat(stats.get('reach', 0), 'Охват', 'blue')}
{format_stat(stats.get('visitors', 0), 'Посетители', 'orange')}
{format_stat(stats.get('views', 0), 'Просмотры', 'green')}

{format_stat(stats.get('likes', 0), 'Лайки', 'red')}
{format_stat(stats.get('shares', 0), 'Репосты', 'violet')}
{format_stat(stats.get('comments', 0), 'Комментарии', 'yellow')}

</div>

{separator_svg}

## ⚙️ Техническая информация

- **Последнее обновление**: {update_time}
- **Источник данных**: VK API
- **Автоматизация**: GitHub Actions
- **Частота обновления**: Ежедневно

> **💡 Разработано IT-специалистами**  
> [![GitHub](https://img.shields.io/badge/GitHub-Repo-brightgreen?logo=github)](https://github.com/rucryptowhale/VK-NPV)
> [![VK](https://img.shields.io/badge/VK-Community-blue?logo=vk)](https://vk.com/netpresentvalue)

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=435&lines=Powered+by+GitHub+Actions;Professional+Analytics;Data+Driven+Decisions" alt="Typing SVG" />
</div>
"""
