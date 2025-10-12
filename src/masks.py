import logging
import os
from datetime import datetime

# Создаем директорию для логов, если её не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл с перезаписью
file_handler = logging.FileHandler("logs/masks.log", mode="w")  # mode='w' обеспечивает перезапись
file_handler.setLevel(logging.DEBUG)

# Форматируем вывод логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_numbers: str) -> str:
    """Маскирует номер банковской карты"""
    try:
        if isinstance(card_numbers, str):
            if len(card_numbers) == 16:
                masked_card_numbers = [card_numbers[:4], card_numbers[4:6] + "**", "****", card_numbers[-4:]]
                logger.info(f"Успешная маскировка карты: {card_numbers}")
                return " ".join(masked_card_numbers)
            else:
                logger.warning(f"Неверный формат карты: {card_numbers}. Длина должна быть 16 символов")
                return "Ошибка. Проверьте, правильно ли вы написали номер карты, и попробуйте снова."
        else:
            logger.error(f"Неверный тип данных: {type(card_numbers)}. Ожидается str")
            return "Ошибка типа данных. Функция принмает данные str"
    except Exception as e:
        logger.exception("Произошла непредвиденная ошибка при маскировке карты")
        return "Произошла ошибка при обработке данных"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета"""
    try:
        if isinstance(account_number, str):
            if len(account_number) == 20:
                masked_account_number = ["**", account_number[-4:]]
                logger.info(f"Успешная маскировка счета: {account_number}")
                return "".join(masked_account_number)
            else:
                logger.warning(f"Неверный формат счета: {account_number}. Длина должна быть 20 символов")
                return "Ошибка. Проверьте, правильно ли вы написали номер счета, и попробуйте снова."
        else:
            logger.error(f"Неверный тип данных: {type(account_number)}. Ожидается str")
            return "Ошибка типа данных. Функция принмает данные str"
    except Exception as e:
        logger.exception("Произошла непредвиденная ошибка при маскировке счета")
        return "Произошла ошибка при обработке данных"
