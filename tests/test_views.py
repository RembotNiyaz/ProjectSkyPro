import pytest
import pandas as pd
from src import views # замените на актуальный импорт

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

def test_events_page_structure(sample_transactions):
    result = views.events_page(sample_transactions)

    # Проверка наличия ключей
    assert "events" in result
    assert "top_categories" in result
    assert "summary" in result

    # Проверка типа данных
    assert isinstance(result["events"], list)
    assert isinstance(result["top_categories"], list)
    assert isinstance(result["summary"], dict)

    # Проверка содержимого
    assert len(result["events"]) == len(sample_transactions.groupby([pd.Grouper(key="Дата операции", freq="D"), "Категория"])["Сумма операции"].sum())
    assert len(result["top_categories"]) <= 5

    # Проверка, что суммы корректны и отсортированы
    top_cats = result["top_categories"]
    totals = [item["total"] for item in top_cats]
    assert totals == sorted(totals, reverse=True)

