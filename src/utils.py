import json
import logging
import os
from typing import Dict, List

# Создаем директорию для логов, если её не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл с перезаписью
file_handler = logging.FileHandler("logs/utils.log", mode="w")  # mode='w' обеспечивает перезапись
file_handler.setLevel(logging.DEBUG)

# Форматируем вывод логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict]: Список словарей с данными транзакций
    """
    try:
        logger.info(f"Попытка загрузить файл: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                logger.info(f"Успешная загрузка данных из файла: {file_path}")
                return data
            else:
                logger.warning(f"Данные в файле {file_path} не являются списком")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при загрузке файла: {file_path}")
        return []
