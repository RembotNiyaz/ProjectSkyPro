import unittest
from unittest.mock import MagicMock, patch

from src.external_api import convert_to_rubles


class TestCurrencyConversion(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые транзакции
        self.rub_transaction = {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}}

        self.usd_transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        self.eur_transaction = {"operationAmount": {"operationAmount": {"amount": 100, "currency": {"code": "EUR"}}}}

    @patch("requests.get")
    def test_rub_conversion(self, mock_get):
        # Для рублей не должно быть запроса к API
        result = convert_to_rubles(self.rub_transaction)
        mock_get.assert_not_called()
        self.assertEqual(result, 100.0)

    @patch("requests.get")
    def test_usd_conversion(self, mock_get):
        # Мокаем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "rates": {"USD": 90.0}}
        mock_get.return_value = mock_response

        result = convert_to_rubles(self.usd_transaction)
        self.assertEqual(result, 9000.0)

    @patch("requests.get")
    def test_invalid_transaction(self, mock_get):
        # Невалидная транзакция
        invalid_transaction = {}

        with self.assertRaises(AttributeError):
            convert_to_rubles(invalid_transaction)
