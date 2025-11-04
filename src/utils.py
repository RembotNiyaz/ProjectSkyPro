import pandas as pd
import json
import logging
import datetime as dt
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import os
import requests

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Returns:
        DataFrame с транзакциями
    """
    file_path = os.getenv("TRANSACTIONS_FILE", "data/operations.xlsx")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций из {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        raise


def get_date_range(date_str: str, period: str = "M") -> tuple:
    """
    Возвращает диапазон дат для анализа.

    Args:
        date_str: дата в формате 'YYYY-MM-DD HH:MM:SS'
        period: 'W' (неделя), 'M' (месяц), 'Y' (год), 'ALL' (всё)

    Returns:
        tuple: (start_date, end_date)
    """
    end_date = dt.datetime.strptime(date_str.split()[0], "%Y-%m-%d")

    if period == "W":
        start_date = end_date - dt.timedelta(days=end_date.weekday())
    elif period == "M":
        start_date = end_date.replace(day=1)
    elif period == "Y":
        start_date = end_date.replace(month=1, day=1)
    elif period == "ALL":
        start_date = dt.datetime(1970, 1, 1)
    else:
        raise ValueError("period должен быть W, M, Y или ALL")

    return start_date, end_date


def greet_by_time() -> str:
    """Возвращает приветствие по времени суток."""
    hour = dt.datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_currency_rates_from_api(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют с сайта (реальный API).

    """
    try:

        response = requests.get('https://api.apilayer.com/exchangerates_data/convert')
        response.raise_for_status()
        data = response.json()
        rates = []

        for curr in currencies:
            rate = data['rates'].get(curr)
            if rate is not None:
                rates.append({"currency": curr, "rate": rate})
            else:
                # Если валюты нет — можно поставить 0 или пропустить
                rates.append({"currency": curr, "rate": None})
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return []