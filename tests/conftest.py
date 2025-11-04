from datetime import datetime as dt

import pandas as pd
import pytest


@pytest.fixture
def sample_excel_file(tmp_path):
    # Создаем временный Excel файл
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    file_path = tmp_path / "operations.xlsx"
    df.to_excel(file_path, index=False)
    return str(file_path)

import pandas as pd
from datetime import datetime as dt

@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "2024-04-01",
            "2024-04-01",
            "2024-04-02",
            "2024-04-02",
            "2024-04-03",
        ],
        "Категория": [
            "еда",
            "транспорт",
            "еда",
            "развлечения",
            "еда",
        ],
        "Сумма операции": [50.0, 20.0, 70.0, 100.0, 30.0],
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df

# Фикстура для данных транзакций для calculate_cashback_categories
@pytest.fixture
def cashback_data():
    return [
        {'Дата операции': '2024-04-01', 'Категория': 'еда', 'Сумма операции': 100.0},
        {'Дата операции': '2024-04-15', 'Категория': 'транспорт', 'Сумма операции': 50.0},
        {'Дата операции': '2024-04-10', 'Категория': 'еда', 'Сумма операции': 200.0},
        {'Дата операции': '2024-03-20', 'Категория': 'развлечения', 'Сумма операции': 300.0},
    ]

@pytest.fixture
def simple_transactions():
    data = {
        'Дата операции': ['2024-01-01', '2024-02-01', '2024-03-01'],
        'Категория': ['еда', 'развлечения', 'еда'],
        'Сумма операции': [100, 200, 150]
    }
    df = pd.DataFrame(data)
    return df
