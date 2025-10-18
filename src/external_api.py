from typing import Dict
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict): Словарь с данными транзакции

    Returns:
        float: Сумма в рублях
    """
    amount = transaction.get("operationAmount").get("amount")
    currency = transaction.get("operationAmount").get("currency").get("code")

    if currency == "RUB":
        return float(amount)

    try:
        response = requests.get(f"{BASE_URL}?access_key={API_KEY}")
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        rate = rates.get(currency)

        if rate:
            return float(amount) * rate
        else:
            raise ValueError("Курс для указанной валюты не найден")
    except requests.RequestException as e:
        print(f"Ошибка при получении курса валют: {e}")
        return float(amount)
