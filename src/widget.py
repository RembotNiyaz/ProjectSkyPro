from masks import get_mask_card_number, get_mask_account


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.
    """
    input_string_list = input_string.split()
    numbers = ""
    card_type = []
    # Разделяем тип и номер
    for number in input_string_list:
        if number.isdigit():
            numbers += number
        elif number.isalpha():
            card_type.append(number)
    # Определяем тип и применяем соответствующую маску
    if len(numbers) == 20:
        return f"{" ".join(card_type)} {get_mask_account(numbers)}"
    else:
        return f"{" ".join(card_type)} {get_mask_card_number(numbers)}"

def get_date(data: str) -> str:
    """принимает на вход строку с датой в формате
       "2024-03-11T02:26:18.671407"
       и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    return f"{data[8:10]}.{data[5:7]}.{data[0:4]}"