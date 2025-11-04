import pytest
from unittest.mock import patch, MagicMock

# Импортировать функцию из модуля
from src.main import run_all_features

@pytest.fixture
def mock_transactions():
    # Возвращает фиктивные транзакции
    return [{"id": 1, "amount": 100, "category": "Кафе"}]

def test_run_all_features(mocker, mock_transactions):
    # Мокаем функции, которые вызываются внутри run_all_features
    mock_load = mocker.patch('src.utils.load_transactions', return_value=mock_transactions)
    mock_main_page = mocker.patch('src.views.main_page', return_value={"page": "main"})
    mock_events_page = mocker.patch('src.views.events_page', return_value={"events": []})
    mock_cashback = mocker.patch('src.services.calculate_cashback_categories', return_value={"cashback": 10})
    mock_investment = mocker.patch('src.services.investment_bank', return_value=50)
    mock_search = mocker.patch('src.services.simple_search', return_value={"results": []})
    mock_spending_category = mocker.patch('src.reports.spending_by_category', return_value={"category": "Кафе"})
    mock_spending_weekday = mocker.patch('src.reports.spending_by_weekday', return_value={"weekday": "Monday"})
    mock_spending_workday = mocker.patch('src.reports.spending_by_workday', return_value={"workday": "Yes"})
    # Мокаем json.dump, чтобы не писать файлы
    mock_json_dump = mocker.patch('json.dump')

    # Вызов тестируемой функции
    run_all_features()

    # Проверяем, что все функции вызвались
    mock_load.assert_called_once()
    mock_main_page.assert_called_once()
    mock_events_page.assert_called_once()
    mock_cashback.assert_called_once()
    mock_investment.assert_called_once()
    mock_search.assert_called_once()
    mock_spending_category.assert_called_once()
    mock_spending_weekday.assert_called_once()
    mock_spending_workday.assert_called_once()
    # Проверяем, что json.dump вызвано нужное количество раз
    assert mock_json_dump.call_count == 5  # По количеству вызовов dump
