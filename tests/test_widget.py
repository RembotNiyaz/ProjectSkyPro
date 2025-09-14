import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_card_account, expected_card_account",
    [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("7158300734726758", "Введите название платежной системы вместе с номером карты"),
        ("MasterCard 715830073472", "Неверный номер карты или счета"),
        ("35383033474447895560", "Счет **5560"),
    ],
)
def test_widget(input_card_account, expected_card_account):
    assert mask_account_card(input_card_account) == expected_card_account


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2022-01-01T00:00:00.000000", "01.01.2022"),
    ],
)
def test_date(input_data, expected):
    assert get_date(input_data) == expected
