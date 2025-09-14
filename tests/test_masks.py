import pytest

from src.widget import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "input_card, expected_masks_card",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000792289606", "Ошибка. Проверьте, правильно ли вы написали номер карты, и попробуйте снова."),
        (7000792289606361, "Ошибка типа данных. Функция принмает данные str"),
    ],
)
def test_function_masks_card(input_card, expected_masks_card):
    assert get_mask_card_number(input_card) == expected_masks_card


@pytest.mark.parametrize(
    "input_account, expected_masks_account",
    [
        ("73654108430135874305", "**4305"),
        ("736541084301358743", "Ошибка. Проверьте, правильно ли вы написали номер счета, и попробуйте снова."),
        (7000792289606361, "Ошибка типа данных. Функция принмает данные str"),
    ],
)
def test_function_masks_account(input_account, expected_masks_account):
    assert get_mask_account(input_account) == expected_masks_account
