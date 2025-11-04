import pandas as pd
import pytest
from datetime import datetime as dt
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
# Простая фикстура для тестовых данных


# Тест для spending_by_category
@pytest.mark.parametrize("category, date", [
    ("еда", "2024-04-10"),
    ("развлечения", "2024-04-10")
])
def test_spending_by_category_simple(simple_transactions, category, date):
    result = spending_by_category(simple_transactions.copy(), category, date)
    assert isinstance(result, dict)
    assert 'total_spent' in result

# Тест для spending_by_weekday
@pytest.mark.parametrize("date", ["2024-04-10"])
def test_spending_by_weekday_simple(simple_transactions, date):
    result = spending_by_weekday(simple_transactions.copy(), date)
    assert isinstance(result, dict)
    assert 'period' in result
    assert 'averages_by_weekday' in result

# Тест для spending_by_workday
@pytest.mark.parametrize("date", ["2024-04-10"])
def test_spending_by_workday_simple(simple_transactions, date):
    result = spending_by_workday(simple_transactions.copy(), date)
    assert isinstance(result, dict)
    assert 'period' in result
    assert 'average_spending' in result
