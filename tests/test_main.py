import unittest
from unittest.mock import patch, MagicMock
from src.main import user_interaction

class TestUserInteraction(unittest.TestCase):

    @patch('builtins.input')
    @patch('your_module.OpenStreetMapAPI')
    @patch('your_module.OpenSkyAPI')
    @patch('your_module.JSONFileSaver')
    @patch('your_module.filter_by_country')
    @patch('your_module.get_top_n')
    def test_user_interaction_flow(self, mock_get_top_n, mock_filter_by_country, mock_JSONFileSaver, mock_OpenSkyAPI, mock_OpenStreetMapAPI, mock_input):
        # Настройка моков входных данных
        mock_input.side_effect = [
            'TestCountry',  # Название страны
            '2',            # Количество самолетов для топ N
            'USA,Canada'    # Страны для фильтрации
        ]

        # Моки API
        mock_osm_api = MagicMock()
        mock_osm_api.get_country_bounding_box.return_value = (10, 20, 30, 40)
        mock_os_api = MagicMock()
        # Возвращаем список "стейтов"
        mock_os_api.get_airplanes_in_bbox.return_value = [
            ('id1', 'CALLSIGN1', 'USA', None, None, None, None, None, None, None, None, None, None, 10000),
            ('id2', 'CALLSIGN2', 'Canada', None, None, None, None, None, None, None, None, None, None, 15000),
            ('id3', 'CALLSIGN3', 'Mexico', None, None, None, None, None, None, None, None, None, None, 5000),
        ]

        # Моки API классов
        mock_OpenStreetMapAPI.return_value = mock_osm_api
        mock_OpenSkyAPI.return_value = mock_os_api

        # Мок фильтрации и топ N
        mock_airplanes = [
            MagicMock(call_sign='CALLSIGN1', registration_country='USA', speed=300, altitude=10000),
            MagicMock(call_sign='CALLSIGN2', registration_country='Canada', speed=350, altitude=15000),
            MagicMock(call_sign='CALLSIGN3', registration_country='Mexico', speed=250, altitude=5000),
        ]
        mock_filter_by_country.return_value = mock_airplanes
        mock_get_top_n.return_value = mock_airplanes[:2]  # Топ 2

        # Мокаем JSONFileSaver
        mock_saver = MagicMock()
        mock_JSONFileSaver.return_value = mock_saver

        # Вызов функции
        user_interaction()

        # Проверки
        # Проверяем, что API вызваны с правильными аргументами
        mock_osm_api.get_country_bounding_box.assert_called_with('TestCountry')
        mock_os_api.get_airplanes_in_bbox.assert_called_with(10, 20, 30, 40)

        # Проверка фильтрации
        mock_filter_by_country.assert_called_with(mock_airplanes, ['USA', 'Canada'])
        # Проверка получения топ N
        mock_get_top_n.assert_called_with(mock_airplanes, 2)

        # Проверка вызова добавления самолетов в файл
        self.assertEqual(mock_saver.add.call_count, 2)
        calls = [call[0][0] for call in mock_saver.add.call_args_list]
        # Проверка, что добавляются правильные объекты
        self.assertTrue(all(isinstance(c, MagicMock) for c in calls))

if __name__ == '__main__':
    unittest.main()