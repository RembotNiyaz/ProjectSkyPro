def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.
    """
    # Разделяем тип и номер
    parts = input_string.split(' ', 1)
    card_type, number = parts
    number = number.replace(' ', '')  # Убираем пробелы из номера

    # Определяем тип и применяем соответствующую маску
    if card_type == "Счет":
        masked_account_number = ["**", number[-4:]]
        return f"{card_type} {"".join(masked_account_number)}"
    else:
        masked_card_numbers = [number[:4], number[4:6] + "**", "****", number[-4:]]
        return f"{card_type} {"".join(masked_card_numbers)}"
