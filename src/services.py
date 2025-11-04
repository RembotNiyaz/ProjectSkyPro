from typing import List, Dict, Any
import pandas as pd
import json
import logging
import re
from datetime import datetime as dt

logger = logging.getLogger(__name__)
# Настройка логгера, если еще не настроен
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def calculate_cashback_categories(
        data: List[Dict[str, Any]],
        year: int,
        month: int
) -> Dict[str, float]:
    """
    Анализирует выгодные категории для кешбэка.

    Args:
        data: список транзакций
        year: год анализа
        month: месяц анализа

    Returns:
        Словарь с категориями и суммой потенциального кешбэка
    """
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Фильтруем по году и месяцу
    mask = (df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)
    monthly_data = df[mask]

    # Группируем по категориям и считаем сумму
    category_spending = monthly_data.groupby('Категория')['Сумма операции'].sum()

    # Кешбэк 1% от суммы
    cashback_by_category = {cat: round(spending * 0.01, 2)
                            for cat, spending in category_spending.items()}

    logger.info(f"Рассчитан кешбэк для {year}-{month}: {cashback_by_category}")
    return cashback_by_category


def investment_bank(
        month: str,
        transactions: List[Dict[str, Any]],
        limit: int
) -> float:
    """
    Рассчитывает сумму, отложенную в «Инвесткопилку» через округление трат.

    Args:
        month: месяц для расчёта в формате 'YYYY-MM'
        transactions: список транзакций с полями:
            - 'Дата операции' (str, формат 'YYYY-MM-DD')
            - 'Сумма операции' (float)
        limit: предел округления (10, 50 или 100)

    Returns:
        Сумма, отложенная в инвесткопилку (float)
    """
    try:
        # Фильтруем транзакции по месяцу
        target_year, target_month = map(int, month.split('-'))
        filtered_txns = []

        for txn in transactions:
            txn_date = dt.strptime(txn['Дата операции'], '%Y-%m-%d')
            if txn_date.year == target_year and txn_date.month == target_month:
                filtered_txns.append(txn)

        total_saved = 0.0

        for txn in filtered_txns:
            amount = txn['Сумма операции']
            # Округляем вверх до ближайшего кратного limit
            rounded = ((amount // limit) + 1) * limit
            saved = rounded - amount
            total_saved += saved

        logger.info(f"Инвесткопилка за {month}: накоплено {round(total_saved, 2)} руб.")
        return round(total_saved, 2)

    except Exception as e:
        logger.error(f"Ошибка в investment_bank: {e}")
        raise


def search_by_phone(
        transactions: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Находит транзакции с телефонными номерами в описании.

    Args:
        transactions: список транзакций

    Returns:
        Словарь с ключом 'phone_transactions' и списком транзакций
    """
    # Регулярное выражение для поиска российских номеров
    phone_pattern = re.compile(
        r'(\+?7[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})'
    )
    results = []

    for txn in transactions:
        desc = str(txn.get('Описание', ''))
        if phone_pattern.search(desc):
            results.append(txn)

    logger.info(f"Поиск по телефонам: найдено {len(results)} транзакций")
    return {"phone_transactions": results}


def search_transfers_to_persons(
        transactions: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Находит переводы физлицам (категория 'Переводы' + имя и фамилия в описании).

    Args:
        transactions: список транзакций

    Returns:
        Словарь с ключом 'person_transfers' и списком транзакций
    """
    namepattern = re.compile(r'[А-Яа-я]+\s[А-Яа-я]\.')
    results = []

    for txn in transactions:
        category = txn.get('Категория', '')
        desc = str(txn.get('Описание', ''))

        if category == 'Переводы' and namepattern.search(desc):
            results.append(txn)

    logger.info(f"Переводы физлицам: найдено {len(results)} транзакций")
    return {"person_transfers": results}

def simple_search(
        transactions: List[Dict[str, Any]],
        query: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Простая поиск транзакций по ключевому слову или фразе в описании.

    Args:
        transactions: список транзакций
        query: строка для поиска в описании

    Returns:
        Словарь с ключом 'results' и списком найденных транзакций
    """
    results = []

    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for txn in transactions:
        desc = str(txn.get('Описание', ''))
        if pattern.search(desc):
            results.append(txn)

    logger.info(f"Поиск по запросу '{query}': найдено {len(results)} транзакций")
    return {"results": results}