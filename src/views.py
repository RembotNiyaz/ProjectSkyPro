import json
from typing import Dict, Any, List
from datetime import datetime as dt
import pandas as pd
import logging
from src.utils import load_transactions, greet_by_time, get_currency_rates_from_api


logger = logging.getLogger(__name__)
# Настройка логгера, если еще не настроен
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют из API."""
    # Здесь должен быть вызов реального API (например, ЦБ РФ или Open Exchange Rates)
    # Для примера возвращаем фиктивные данные
    return [{"currency": curr, "rate": round(70 + (hash(curr) % 10), 2)} for curr in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций из API."""
    # Здесь должен быть вызов реального API (например, Yahoo Finance или Alpha Vantage)
    # Для примера возвращаем фиктивные данные
    return [{"stock": stock, "price": round(100 + (hash(stock) % 1000), 2)} for stock in stocks]


def main_page(date_str: str) -> Dict[str, Any]:
    """
    Главная страница: возвращает JSON с приветствием, данными по картам, топ‑транзакциями,
    курсами валют и ценами акций.
    """

    # 1. Приветствие
    greeting = greet_by_time()

    # 2. Загружаем транзакции
    df = load_transactions()

    # Фильтруем по дате (с начала месяца до указанной даты)
    end_date = dt.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1)
    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    monthly_df = df[mask]

    # 3. Данные по картам
    cards_data = []
    card_groups = monthly_df.groupby("Номер карты")
    for card_num, group in card_groups:
        total_spent = group["Сумма операции"].sum()
        cashback = round(total_spent * 0.01, 2)  # 1% кешбэка
        cards_data.append(
            {"last_digits": str(card_num)[-4:], "total_spent": round(total_spent, 2), "cashback": cashback}
        )

    # 4. Топ‑5 транзакций по сумме
    top_transactions = monthly_df.nlargest(5, "Сумма операции")
    top_list = []
    for _, row in top_transactions.iterrows():
        top_list.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    # 5. Курсы валют — вызываем API
    try:
        with open("user_settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
        currencies = settings["user_currencies"]
        currency_rates = get_currency_rates_from_api(currencies)
    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        currency_rates = []

    # 6. Цены акций
    try:
        stocks = settings["user_stocks"]
        stock_prices = get_stock_prices(stocks)
    except Exception as e:
        print(f"Ошибка при получении цен акций: {e}")
        stock_prices = []

    # Итоговый результат
    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_list,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        "summary": {
            "total_spent": round(monthly_df["Сумма операции"].sum(), 2),
            "average_transaction": round(monthly_df["Сумма операции"].mean(), 2),
            "transaction_count": len(monthly_df),
            "cashback_total": round(sum(card["cashback"] for card in cards_data), 2),
        },
    }

    logger.info(
        f"Главная страница: сформировано {len(cards_data)} карт, "
        f"{len(top_list)} топ‑транзакций, период {start_date.date()}–{end_date.date()}"
    )
    return result


def events_page(transactions: pd.DataFrame) -> Dict[str, Any]:
    """
    Страница «События»: возвращает JSON с агрегированными данными по транзакциям.
    Группирует транзакции по дате и категории, считает суммы.
    """
    # Группируем по дате и категории
    grouped = (
        transactions.groupby([pd.Grouper(key="Дата операции", freq="D"), "Категория"])["Сумма операции"]
        .sum()
        .reset_index()
    )

    # Преобразуем в список словарей
    events_list = []
    for _, row in grouped.iterrows():
        events_list.append(
            {
                "date": row["Дата операции"].strftime("%Y-%m-%d"),
                "category": row["Категория"],
                "amount": round(row["Сумма операции"], 2),
            }
        )

    # Топ‑5 категорий по сумме
    category_totals = transactions.groupby("Категория")["Сумма операции"].sum()
    top_categories = category_totals.nlargest(5).round(2).to_dict()

    result = {
        "events": events_list,
        "top_categories": [{"category": cat, "total": total} for cat, total in top_categories.items()],
        "summary": {
            "total_transactions": len(transactions),
            "total_amount": round(transactions["Сумма операции"].sum(), 2),
            "unique_categories": len(category_totals),
        },
    }

    logger.info(f"Страница «События»: {len(events_list)} событий, " f"{len(top_categories)} топ‑категорий")
    return result
