from datetime import datetime


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


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа
    """
    cleaned_string = "".join(char for char in input_string if char.isdigit() or char in (" ", "-"))
    input_name_list = input_string.split()
    input_string_list = cleaned_string.replace("-", " ").split()
    numbers = ""
    card_type = []
    # Разделяем тип и номер
    for number in input_string_list:
        if number.isdigit():
            numbers += number
    for name in input_name_list:
        if name.isalpha():
            card_type.append(name)
    # Определяем тип и применяем соответствующую маску
    if len(numbers) == 20:
        if len(card_type) == 0:
            return f"Счет {get_mask_account(numbers)}"
        else:
            return f"{" ".join(card_type)} {get_mask_account(numbers)}"

    elif len(numbers) == 16:
        if len(card_type) == 0:
            return "Введите название платежной системы вместе с номером карты"
        else:
            return f"{" ".join(card_type)} {get_mask_card_number(numbers)}"
    else:
        return "Неверный номер карты или счета"


def get_date(date_str: str) -> str:
    """функция преобразования даты формата "2018-07-11T02:26:18.671407" в формат "11.07.2018" """

    input_format = "%Y-%m-%dT%H:%M:%S.%f"
    date_obj = datetime.strptime(date_str, input_format)
    output_format = "%d.%m.%Y"
    return date_obj.strftime(output_format)
