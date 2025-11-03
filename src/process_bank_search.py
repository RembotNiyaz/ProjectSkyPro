import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Функция для поиска банковских операций по строке в описании с использованием регулярных выражений.

    Параметры:
    data (List[Dict]) - список словарей с данными о банковских операциях
    search (str) - строка для поиска в описании операций

    Возвращает:
    List[Dict] - отфильтрованный список словарей, содержащих искомую строку в описании
    """
    # Создаем регулярное выражение с учетом регистра и границ слов
    # re.IGNORECASE - игнорируем регистр при поиске
    # \b - ищем целые слова
    pattern = re.compile(rf"\b{re.escape(search)}\b", re.IGNORECASE)

    # Фильтруем операции, оставляя только те, где есть совпадение в описании
    result = [
        operation for operation in data if "description" in operation and pattern.search(operation["description"])
    ]

    return result
