import unittest
from unittest.mock import patch

from src.external_api import convert_to_rubles


class TestExternalAPI(unittest.TestCase):

    @patch("requests.get")
    def test_convert_rub(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"RUB": 1}}
        transaction = {"amount": 100, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 100.0)  # Проверяем, что сумма в рублях равна исходной

    @patch("requests.get")
    def test_convert_usd(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"USD": 90}}
        transaction = {"amount": 1, "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 90.0)  # 1 USD = 90 RUB

    @patch("requests.get")
    def test_convert_eur(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"EUR": 100}}
        transaction = {"amount": 2, "currency": "EUR"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 200.0)  # 2 EUR = 200 RUB

    def test_missing_currency(self):
        transaction = {"amount": 100}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 100.0)  # По умолчанию считаем, что валюта RUB

    def test_missing_amount(self):
        transaction = {"currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 0.0)  # При отсутствии суммы возвращаем 0
