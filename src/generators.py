def filter_by_currency(transactions, currency_code):
    """
    Фильтрует транзакции по указанной валюте.

    :param transactions: список словарей с транзакциями
    :param currency_code: код валюты для фильтрации (например, 'USD')
    :return: итератор по отфильтрованным транзакциям
    """
    for transaction in transactions:
        # Проверяем наличие вложенных словарей и корректность структуры
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
        ):
            # Сравниваем код валюты
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction


def transaction_descriptions(transactions):
    """
    Генератор, возвращающий описания транзакций по очереди.

    :param transactions: список словарей с транзакциями
    :return: итератор по описаниям операций
    """
    for transaction in transactions:
        # Проверяем наличие ключа description в каждой транзакции
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: начальное значение диапазона (целое число)
    :param end: конечное значение диапазона (целое число)
    """
    if start < 1 or end > 9999999999999999:
        raise ValueError("Значения должны быть в диапазоне от 1 до 9999999999999999")

    for number in range(start, end + 1):
        # Форматируем число в строку с ведущими нулями
        formatted_number = f"{number:016d}"
        # Разбиваем на группы по 4 символа и добавляем пробелы
        card_number = (
            f"{formatted_number[0:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:16]}"
        )
        yield card_number


