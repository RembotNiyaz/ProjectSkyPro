import pytest
from unittest.mock import patch, MagicMock

def test_user_interaction():
    with patch('src.api.OpenStreetMapAPI') as mock_osm_cls, \
         patch('src.api.OpenSkyAPI') as mock_opensky_cls, \
         patch('src.utils.filter_by_country') as mock_filter, \
         patch('src.utils.get_top_n') as mock_get_top, \
         patch('src.file_savers.JSONFileSaver') as mock_saver_cls, \
         patch('builtins.input', side_effect=["USA", "2", "USA,Canada"]):

        # Мокаем экземпляры API
        mock_osm_instance = mock_osm_cls.return_value
        mock_osm_instance.get_country_bounding_box.return_value = [-10.0, 10.0, -20.0, 20.0]

        mock_opensky_instance = mock_opensky_cls.return_value
        mock_opensky_instance.get_airplanes_in_bbox.return_value = [
            ("id1", "CALLSIGN1", "USA", None, None, None, None, None, None, 500, None, None, None, 10000),
            ("id2", "CALLSIGN2", "USA", None, None, None, None, None, None, 300, None, None, None, 8000),
            ("id3", "CALLSIGN3", "Canada", None, None, None, None, None, None, 600, None, None, None, 12000)
        ]

        # Мокаем фильтр и выбор топ N
        mock_filter.return_value = [
            MagicMock(call_sign="CALLSIGN1", registration_country="USA", speed=500, altitude=10000),
            MagicMock(call_sign="CALLSIGN2", registration_country="USA", speed=300, altitude=8000),
            MagicMock(call_sign="CALLSIGN3", registration_country="Canada", speed=600, altitude=12000)
        ]
        mock_get_top.return_value = [
            MagicMock(call_sign="CALLSIGN1", registration_country="USA", speed=500, altitude=10000),
            MagicMock(call_sign="CALLSIGN3", registration_country="Canada", speed=600, altitude=12000)
        ]

        # Мокаем работу с файлом
        mock_saver_instance = mock_saver_cls.return_value

        # Импортируем и вызываем функцию
        from src import main
        main.user_interaction()

        # Проверки
        mock_osm_cls.assert_called_once()
        mock_osm_instance.get_country_bounding_box.assert_called_with("USA")
        mock_opensky_cls.assert_called_once()
        mock_opensky_instance.get_airplanes_in_bbox.assert_called_with(-10.0, 10.0, -20.0, 20.0)
        # Проверки фильтров и сохранения
        assert mock_filter.called
        assert mock_get_top.called
        assert mock_saver_instance.add.call_count == 2