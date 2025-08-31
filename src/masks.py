def get_mask_card_number(card_numbers: str) -> str:
    """Маскирует номер банковской карты"""

    masked_card_numbers = [card_numbers[:4], card_numbers[4:6] + "**", "****", card_numbers[-4:]]

    return " ".join(masked_card_numbers)


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета"""

    masked_account_number = ["**", account_number[-4:]]

    return "".join(masked_account_number)
