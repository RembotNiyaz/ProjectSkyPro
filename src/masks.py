def get_mask_card_number(card_numbers: str) -> str:
    """Маскирует номер банковской карты"""

    if type(card_numbers) == str:
        if len(card_numbers) == 16:
            masked_card_numbers = [card_numbers[:4], card_numbers[4:6] + "**", "****", card_numbers[-4:]]
            return " ".join(masked_card_numbers)
        else:
            return "Ошибка. Проверьте, правильно ли вы написали номер карты, и попробуйте снова."
    else:
        return "Ошибка типа данных. Функция принмает данные str"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета"""
    if type(account_number) == str:
        if len(account_number) == 20:
            masked_account_number = ["**", account_number[-4:]]
            return "".join(masked_account_number)
        else:
            return "Ошибка. Проверьте, правильно ли вы написали номер счета, и попробуйте снова."
    else:
        return "Ошибка типа данных. Функция принмает данные str"
