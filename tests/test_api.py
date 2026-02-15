import unittest
from unittest.mock import patch, Mock
from src.api import BaseAPI, OpenStreetMapAPI, OpenSkyAPI

class TestAPIs(unittest.TestCase):

    @patch('requests.Session.get')
    def test_get_country_bounding_box_success(self, mock_get):
        # Мокаем успешный ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "boundingbox": ["10.0", "20.0", "30.0", "40.0"]
        }]
        mock_get.return_value = mock_response

        api = OpenStreetMapAPI()
        bbox = api.get_country_bounding_box("Russia")
        self.assertEqual(bbox, [10.0, 20.0, 30.0, 40.0])
        mock_get.assert_called_once()

    @patch('requests.Session.get')
    def test_get_country_bounding_box_no_data(self, mock_get):
        # Мокаем ответ с пустым списком
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        api = OpenStreetMapAPI()
        with self.assertRaises(ValueError):
            api.get_country_bounding_box("UnknownCountry")

    @patch('requests.Session.get')
    def test_get_country_bounding_box_error_status(self, mock_get):
        # Мокаем ошибку
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = OpenStreetMapAPI()
        with self.assertRaises(ConnectionError):
            api.get_country_bounding_box("Russia")

    @patch('requests.Session.get')
    def test_get_airplanes_in_bbox_success(self, mock_get):
        # Мокаем успешный ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "states": [
                ["abc", "call_sign1", "RU", None, None, None, None, None, None, 600, None, None, None, 30000],
                ["def", "call_sign2", "US", None, None, None, None, None, None, 550, None, None, None, 28000]
            ]
        }
        mock_get.return_value = mock_response

        api = OpenSkyAPI()
        states = api.get_airplanes_in_bbox(10, 20, 30, 40)
        self.assertEqual(len(states), 2)
        self.assertEqual(states[0][1], "call_sign1")
        self.assertEqual(states[1][2], "US")
        mock_get.assert_called_once()

    @patch('requests.Session.get')
    def test_get_airplanes_in_bbox_error_status(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = OpenSkyAPI()
        with self.assertRaises(ConnectionError):
            api.get_airplanes_in_bbox(0, 0, 0, 0)

if __name__ == '__main__':
    unittest.main()