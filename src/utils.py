import json
from typing import Dict, List


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict]: Список словарей с данными транзакций
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
