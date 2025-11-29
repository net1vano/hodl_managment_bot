from datetime import datetime, time


def ensure_min_8am(dt: datetime) -> datetime:
    # Создаём время 08:00
    eight_am = time(8, 0)

    # Если время в dt < 08:00 — заменяем на 08:00 того же дня
    if dt.time() < eight_am:
        return dt.replace(hour=8, minute=0, second=0, microsecond=0)
    return dt

def start_timer():
    """
    Возвращает текущее время для начала таймера.
    """
    return datetime.now()

def calculate_duration(start_time: datetime, end_time: datetime) -> float:
    """
    Возвращает разницу в часах между двумя временами.
    Если разница < 30 минут — возвращает 0.
    Если разница >= 30 минут — округляет до ближайшего целого числа (11.6 -> 12, 10.3 -> 10).
    Если результат > 14 часов — возвращает 14.
    """
    diff = end_time - ensure_min_8am(start_time)
    total_seconds = diff.total_seconds()

    # Проверка: если меньше 30 минут (1800 секунд)
    if total_seconds < 1800:
        return 0.0

    # Считаем часы
    hours = total_seconds / 3600

    # Округляем до ближайшего целого
    rounded_hours = round(hours)

    # Проверка: если больше 14 часов
    if rounded_hours > 14:
        return 14.0

    return float(rounded_hours)

def current_month():
    return datetime.now().month

def current_year():
    return datetime.now().year

from datetime import datetime

def subtract_months(date: datetime, months: int) -> datetime:
    # Вычисляем год и месяц
    total_months = date.month - months
    year = date.year + total_months // 12
    month = total_months % 12

    if month <= 0:
        month += 12
        year -= 1

    # Всегда используем **первый день месяца**
    return date.replace(year=year, month=month, day=1)

# Пример
now = datetime(2025, 3, 31)  # 31 марта 2025
result = subtract_months(now, 2)

POSITIONS = {
    "main_worker": "Основной бариста",
    "helper_worker": "Помощник бариста",
    "newbie": "Стажер"
}


