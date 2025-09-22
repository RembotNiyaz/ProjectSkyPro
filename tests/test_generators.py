import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тесты для filter_by_currency
def test_filter_by_currency(sample_transactions):
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    result = list(usd_transactions)
    assert len(result) == 2
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_filter_by_currency_no_matches(sample_transactions):
    rub_transactions = filter_by_currency(sample_transactions, "EUR")
    result = list(rub_transactions)
    assert len(result) == 0


def test_filter_missing_currency_field(sample_transactions):
    # Проверяем обработку транзакций без поля currency
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2  # Транзакция с ID 789456123 должна быть пропущена


def test_filter_missing_operation_amount(sample_transactions):
    # Проверяем обработку транзакций без operationAmount
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2  # Транзакция с ID 321654987 должна быть пропущена


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions):
    descriptions = transaction_descriptions(sample_transactions)
    result = list(descriptions)
    assert result == ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]


def test_empty_transactions_list():
    empty_transactions = []
    descriptions = transaction_descriptions(empty_transactions)
    result = list(descriptions)
    assert len(result) == 0





test_cases = [
    # Базовый случай
    (1, 1, ["0000 0000 0000 0001"]),
    # Диапазон из нескольких значений
    (1234, 1236, ["0000 0000 0000 1234", "0000 0000 0000 1235", "0000 0000 0000 1236"]),
    # Граничные значения
    (1000000000000000, 1000000000000001, ["1000 0000 0000 0000", "1000 0000 0000 0001"]),
    # Значения с разными длинами
    (999, 1001, ["0000 0000 0000 0999", "0000 0000 0000 1000", "0000 0000 0000 1001"]),
    # Максимальное значение
    (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
]


@pytest.mark.parametrize("start, end, expected", test_cases)
def test_card_number_generator(start, end, expected):
    # Получаем результат работы генератора
    result = list(card_number_generator(start, end))


def test_card_number_generator():
    generator = card_number_generator(1, 3)
    result = list(generator)
    assert result == ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]


def test_card_number_generator():
    # Базовый тест с одним значением
    gen = card_number_generator(1, 1)
    result = next(gen)
    assert result == "0000 0000 0000 0001"

    # Тест с несколькими значениями
    gen = card_number_generator(1234, 1236)
    results = list(gen)
    assert results == ["0000 0000 0000 1234", "0000 0000 0000 1235", "0000 0000 0000 1236"]

    # Проверка формата номера
    for card in results:
        assert len(card) == 19  # 16 цифр + 3 пробела
        assert card.count(" ") == 3
        assert card.replace(" ", "").isdigit()


def test_boundary_values():
    # Проверка граничных значений
    gen = card_number_generator(1000000000000000, 1000000000000001)
    results = list(gen)
    assert results == ["1000 0000 0000 0000", "1000 0000 0000 0001"]
