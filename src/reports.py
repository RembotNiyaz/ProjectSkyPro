import json
from functools import wraps
from datetime import datetime as dt
import os
from typing import Optional, Dict, Any
import pandas as pd
import logging

# Настройка логгера (если не настроен)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результата функции в JSON-файл.

    Args:
        filename: имя файла (если None — генерируется автоматически)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Генерируем имя файла
            if filename is None:
                timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
                fname = f"report_{func.__name__}_{timestamp}.json"
            else:
                fname = filename

            # Сохраняем в файл
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            logger.info(f"Отчёт сохранён в файл: {fname}")
            return result
        return wrapper
    return decorator

@save_report()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict[str, Any]:
    if date is None:
        end_date = dt.now()
    else:
        end_date = dt.strptime(date, '%Y-%m-%d')

    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

    mask = (
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category)
    )
    filtered = transactions[mask].copy()

    # Преобразуем 'Дата операции' в строки
    filtered['Дата операции'] = filtered['Дата операции'].dt.strftime('%Y-%m-%d')

    total = float(filtered['Сумма операции'].sum())

    result = {
        "category": category,
        "period": f"{start_date.strftime('%Y-%m-%d')} — {end_date.strftime('%Y-%m-%d')}",
        "total_spent": round(total, 2),
        "transaction_count": len(filtered),
        "transactions": filtered.to_dict('records')
    }
    return result

@save_report()
def spending_by_weekday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Средние траты по дням недели за последние 3 месяца.
    """
    if date is None:
        end_date = dt.now()
    else:
        end_date = dt.strptime(date, '%Y-%m-%d')

    start_date = end_date - pd.DateOffset(months=3)

    # Убедитесь, что 'Дата операции' — это datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

    # Фильтруем по дате
    mask = (transactions['Дата операции'] >= start_date) & \
           (transactions['Дата операции'] <= end_date)
    filtered = transactions[mask].copy()

    # Добавляем столбец с днём недели
    filtered['День недели'] = filtered['Дата операции'].dt.dayofweek  # 0=Пн, 6=Вс
    filtered['День недели название'] = filtered['Дата операции'].dt.day_name()

    # Группируем по дню недели и считаем сумму трат
    grouped = filtered.groupby('День недели').agg({
        'Сумма операции': 'sum',
        'День недели название': 'first'
    }).reset_index()

    # Считаем среднее за 3 месяца (делим на 3)
    grouped['Среднее за месяц'] = (grouped['Сумма операции'] / 3).round(2)

    result = {
        "period": f"{start_date.date()} — {end_date.date()}",
        "averages_by_weekday": [
            {
                "day_number": int(row['День недели']),
                "day_name": row['День недели название'],
                "average_monthly_spending": float(row['Среднее за месяц'])
            }
            for _, row in grouped.iterrows()
        ]
    }

    logger.info(f"Средние траты по дням недели за {start_date.date()}–{end_date.date()}")
    return result

@save_report()
def spending_by_workday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Средние траты в рабочий и выходной день за последние 3 месяца.
    """
    if date is None:
        end_date = dt.now()
    else:
        end_date = dt.strptime(date, '%Y-%m-%d')

    start_date = end_date - pd.DateOffset(months=3)

    # Убедитесь, что 'Дата операции' — это datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

    # Фильтруем по дате
    mask = (transactions['Дата операции'] >= start_date) & \
           (transactions['Дата операции'] <= end_date)
    filtered = transactions[mask].copy()

    # Определяем, рабочий день или выходной
    filtered['Рабочий день'] = filtered['Дата операции'].dt.weekday < 5  # Пн-Пт = True

    # Группируем и считаем суммы и количества
    grouped = filtered.groupby('Рабочий день')['Сумма операции'].sum()
    counts = filtered.groupby('Рабочий день').size()

    # Вычисляем средние траты
    averages = {}
    for is_workday in [True, False]:
        total = grouped.get(is_workday, 0)
        count = counts.get(is_workday, 0)
        avg = total / count if count > 0 else 0
        key = "workday" if is_workday else "weekend"
        averages[key] = round(avg, 2)

    result = {
        "period": f"{start_date.date()} — {end_date.date()}",
        "average_spending": {
            "workday": averages.get("workday", 0),
            "weekend": averages.get("weekend", 0)
        }
    }

    logger.info(f"Средние траты: рабочий день — {result['average_spending']['workday']} руб., "
                f"выходной — {result['average_spending']['weekend']} руб.")
    return result