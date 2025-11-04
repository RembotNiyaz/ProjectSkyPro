import pytest
from src.services import calculate_cashback_categories, investment_bank, search_by_phone, search_transfers_to_persons



@pytest.mark.parametrize("year, month, expected", [
    (2024, 4, {'еда': 3.0, 'транспорт': 0.5}),
    (2024, 3, {'развлечения': 3.0}),
])
def test_calculate_cashback_categories(cashback_data, year, month, expected):
    result = calculate_cashback_categories(cashback_data, year, month)
    assert isinstance(result, dict)
    assert result == expected

# Тестовые транзакции для investment_bank
transactions = [
    {'Дата операции': '2024-04-01', 'Сумма операции': 47},
    {'Дата операции': '2024-04-15', 'Сумма операции': 102},
    {'Дата операции': '2024-04-20', 'Сумма операции': 33},
    {'Дата операции': '2024-03-25', 'Сумма операции': 50},
]



# Тестовые транзакции для поиска по телефону
transactions_with_phones = [
    {'Описание': 'Платеж +7 (999) 123-45-67'},
    {'Описание': 'Покупка в магазине'},
    {'Описание': 'Перевод +7 912 345 67 89'},
]

@pytest.mark.parametrize("transactions_input, expected_count", [
    (transactions_with_phones, 2),
])
def test_search_by_phone(transactions_input, expected_count):
    result = search_by_phone(transactions_input)
    assert isinstance(result, dict)
    assert isinstance(result['phone_transactions'], list)
    assert len(result['phone_transactions']) == expected_count

# Тестовые транзакции для переводов физлицам
transactions_transfers = [
    {'Категория': 'Переводы', 'Описание': 'Иванов И.И.'},
    {'Категория': 'Переводы', 'Описание': 'Петров П.П.'},
    {'Категория': 'Покупки', 'Описание': 'Магазин'},
]

@pytest.mark.parametrize("transactions_input, expected_count", [
    (transactions_transfers, 2),
])
def test_search_transfers_to_persons(transactions_input, expected_count):
    result = search_transfers_to_persons(transactions_input)
    assert isinstance(result, dict)
    assert isinstance(result['person_transfers'], list)
    assert len(result['person_transfers']) == expected_count