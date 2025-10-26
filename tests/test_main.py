import unittest
from unittest.mock import MagicMock, patch

from main import main

# Предположим, что весь ваш код находится в файле main.py
# И вы экспортировали функцию main() или его часть для тестирования
# Например, создадим обертку:


def main_wrapper():
    return main()


class TestTransactionProcessing(unittest.TestCase):

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.utils.load_transactions")
    @patch("src.reading_financial.read_csv_transactions")
    @patch("src.reading_financial.read_excel_transactions")
    @patch("src.processing.filter_by_state")
    @patch("src.processing.sort_by_date")
    @patch("src.widget.get_date")
    @patch("src.widget.mask_account_card")
    @patch("src.process_bank_search")
    def test_full_flow_json(
        self,
        mock_search,
        mock_mask_card,
        mock_get_date,
        mock_sort,
        mock_filter,
        mock_read_excel,
        mock_read_csv,
        mock_load,
        mock_print,
        mock_input,
    ):
        # Мокаем последовательность вводов пользователя
        mock_input.side_effect = [
            "1",  # выбор JSON
            "EXECUTED",  # статус
            "да",  # сортировать
            "по убыванию",  # сортировка по убыванию
            "да",  # только рубли
            "нет",  # фильтр по слову
        ]

        # Мокаем возвращаемые значения функций
        mock_load.return_value = [
            {
                "date": "2023-01-01",
                "description": "desc",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "1234567890",
                "to": "0987654321",
            }
        ]
        mock_filter.return_value = mock_load.return_value
        mock_sort.return_value = mock_load.return_value
        mock_get_date.return_value = "01.01.2023"
        mock_mask_card.side_effect = lambda x: "****1234" if x else ""
        mock_search.return_value = mock_load.return_value

        result = main()

        # Проверяем, что результат содержит ожидаемые строки
        self.assertIn("Всего банковских операций в выборке: 1", result)
        self.assertIn("01.01.2023", result)
        self.assertIn("desc", result)
        self.assertIn("****1234 -> ****1234", result)

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.utils.load_transactions")
    def test_invalid_choice(self, mock_print, mock_input, mock_load):
        mock_input.return_value = "5"  # некорректный выбор
        result = main()
        self.assertIsNone(result)
        mock_print.assert_any_call("Некорректный выбор.")
