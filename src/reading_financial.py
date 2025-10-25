from typing import Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Считывает транзакции из CSV файла
    """
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient="records")

        for transaction in transactions:
            if not all(key in transaction for key in ["amount", "currency"]):
                raise ValueError("Файл содержит некорректные данные")

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        raise ValueError("Файл пуст")


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Считывает транзакции из Excel файла
    """
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")

        for transaction in transactions:
            if not all(key in transaction for key in ["amount", "currency"]):
                raise ValueError("Файл содержит некорректные данные")

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        raise ValueError("Файл пуст")


if __name__ == "__main__":
    # Пример использования
    try:
        csv_transactions = read_csv_transactions("transactions.csv")
        print("Транзакции из CSV:")
        for tx in csv_transactions[:5]:
            print(tx)

        xlsx_transactions = read_excel_transactions("transactions_excel.xlsx")
        print("\nТранзакции из XLSX:")
        for tx in xlsx_transactions[:5]:
            print(tx)

    except Exception as e:
        print(f"Ошибка: {str(e)}")
