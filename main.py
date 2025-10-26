from src.process_bank_search import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.reading_financial import read_csv_transactions, read_excel_transactions
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    choice = input("Пользователь: ")
    # В зависимости от выбора, читаем файл
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = "data/operations.json"
        transactions = load_transactions(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = "data/transactions.csv"
        transactions = read_csv_transactions(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = "data/transactions_excel.xlsx"
        transactions = read_excel_transactions(file_path)
    else:
        print("Некорректный выбор.")
        return

    # Фильтр по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию:\nДоступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
        ).upper()
        if status_input in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status_input}" ')
            filtered_transactions = filter_by_state(transactions, meaning=status_input)
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')
            print(
                "Введите статус, по которому необходимо выполнить фильтрацию. \nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )

    sort_order = input("Отсортировать операции по дате? Да/Нет\n").lower()
    if sort_order == "да":
        order = input("Отсортировать по возрастанию или по убыванию?\n").lower()
        reverse_sort = True if order == "по убыванию" else False
        # Используем функцию сортировки
        filtered_transactions = sort_by_date(filtered_transactions, state=reverse_sort)

    filter_rub = input("Выводить только рублевые транзакции? Да/Нет\n").lower()
    if filter_rub == "да":
        filtered_transactions = [
            transaction for transaction in filtered_transactions if transaction.get("currency") == "RUB"
        ]

    filter_keyword = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").lower()
    if filter_keyword == "да":
        keyword = input("Введите слово для поиска в описании:\n").lower()
        filtered_transactions = process_bank_search(filtered_transactions, search=keyword)

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    report_lines = []
    report_lines.append("Распечатываю итоговый список транзакций...")
    report_lines.append(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
    for f in filtered_transactions:
        date = get_date(f.get("date", ""))
        description = f.get("description", "")
        amount = f.get("operationAmount", {}).get("amount", "")
        currency = f.get("operationAmount", {}).get("currency", {}).get("code", "")
        from_card = mask_account_card(f.get("from", ""))
        to_card = mask_account_card(f.get("to", ""))
        if len(from_card) > 0:
            report_lines.append(f"{date} {description}\n{from_card} -> {to_card}\nСумма: {amount} {currency}\n")
        else:
            report_lines.append(f"{date} {description}\nСумма: {amount} {currency}\n")
    return "\n".join(report_lines)
