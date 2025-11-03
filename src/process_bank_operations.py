from typing import List, Dict
from collections import Counter
import re


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Функция для подсчета количества операций по категориям с использованием регулярных выражений.

    Параметры:
    data (List[Dict]) - список словарей с данными о банковских операциях
    categories (List[str]) - список категорий для подсчета

    Возвращает:
    Dict[str, int] - словарь с количеством операций по каждой категории
    """
    # Создаем пустой Counter для подсчета
    counter = Counter()

    # Компилируем регулярное выражение для каждой категории
    patterns = {category: re.compile(rf'\b{re.escape(category)}\b', re.IGNORECASE)
                for category in categories}

    # Проходим по каждой операции
    for operation in data:
        description = operation.get('description', '')

        # Проверяем наличие каждой категории в описании
        for category, pattern in patterns.items():
            if pattern.search(description):
                counter[category] += 1

    # Преобразуем Counter в обычный словарь с заданными категориями
    result = {category: counter[category] for category in categories}

    return result

