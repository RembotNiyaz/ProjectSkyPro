import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.reading_financial import read_csv_transactions, read_excel_transactions


class TestTransactionsReader(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.test_csv_data = pd.DataFrame({"amount": [100, 200, 300], "currency": ["RUB", "USD", "EUR"]})

        self.test_xlsx_data = pd.DataFrame({"amount": [400, 500, 600], "currency": ["GBP", "JPY", "CHF"]})

    @patch("pandas.read_csv")
    def test_read_csv_success(self, mock_read_csv):
        mock_read_csv.return_value = self.test_csv_data
        result = read_csv_transactions("test.csv")

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]["amount"], 100)
        self.assertEqual(result[0]["currency"], "RUB")

    @patch("pandas.read_excel")
    def test_read_excel_success(self, mock_read_excel):
        mock_read_excel.return_value = self.test_xlsx_data
        result = read_excel_transactions("test.xlsx")

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]["amount"], 400)
        self.assertEqual(result[0]["currency"], "GBP")

    @patch("pandas.read_csv")
    def test_csv_missing_columns(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({"amount": [100, 200], "type": ["debit", "credit"]})

        with self.assertRaises(ValueError):
            read_csv_transactions("test.csv")

    @patch("pandas.read_excel")
    def test_excel_missing_columns(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({"currency": ["RUB", "USD"], "date": ["2023-01-01", "2023-01-02"]})

        with self.assertRaises(ValueError):
            read_excel_transactions("test.xlsx")

    @patch("pandas.read_csv")
    def test_csv_empty_file(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.EmptyDataError

        with self.assertRaises(ValueError):
            read_csv_transactions("empty.csv")

    @patch("pandas.read_excel")
    def test_excel_empty_file(self, mock_read_excel):
        mock_read_excel.side_effect = pd.errors.EmptyDataError

        with self.assertRaises(ValueError):
            read_excel_transactions("empty.xlsx")

    def test_csv_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_csv_transactions("nonexistent.csv")

    def test_excel_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_excel_transactions("nonexistent.xlsx")
