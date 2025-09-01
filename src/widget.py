from datetime import datetime

from masks import get_mask_account, get_mask_card_number


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


def get_date(date_str: str) -> str:
    """функция преобразования даты формата "2018-07-11T02:26:18.671407" в формат "11.07.2018" """
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")

    # Форматируем объект datetime в нужный формат "ДД.ММ.ГГГГ"
    formatted_date = date_obj.strftime("%d.%m.%Y")

    return formatted_date
