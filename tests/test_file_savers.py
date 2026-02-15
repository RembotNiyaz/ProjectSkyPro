import unittest
from unittest.mock import mock_open, patch
import json
from src.file_savers import JSONFileSaver

# Предположим, что класс Airplane реализует метод to_dict()
class Airplane:
    def __init__(self, call_sign):
        self.call_sign = call_sign

    def to_dict(self):
        return {"call_sign": self.call_sign}

class TestJSONFileSaver(unittest.TestCase):

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_initialization_creates_file_if_not_exists(self, mock_open_fn, mock_exists):
        mock_exists.return_value = False
        # Создаем экземпляр
        saver = JSONFileSaver("test_airplanes.json")
        # Проверяем, что файл создался для записи
        mock_open_fn.assert_called_with("test_airplanes.json", "w")
        handle = mock_open_fn()
        # Проверяем, что внутри вызван json.dump([]), то есть файл инициализируется пустым списком
        handle.write.assert_called()
        # Десериализуем содержимое вызова write
        args, _ = handle.write.call_args
        written_data = args[0]
        data = json.loads(written_data)
        self.assertEqual(data, [])  # должно быть пустым списком

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_all_returns_data(self, mock_open_fn, mock_exists):
        mock_exists.return_value = True
        mock_open_fn.return_value.read.return_value = json.dumps([{"call_sign": "ABC"}])
        saver = JSONFileSaver("test_airplanes.json")
        data = saver.get_all()
        self.assertEqual(data, [{"call_sign": "ABC"}])
        mock_open_fn.assert_called_with("test_airplanes.json", "r")


    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_add_duplicate_does_not_add(self, mock_open_fn, mock_exists):
        mock_exists.return_value = True
        mock_open_fn.return_value.read.return_value = json.dumps([{"call_sign": "DUP"}])
        saver = JSONFileSaver("test_airplanes.json")
        plane = Airplane("DUP")
        saver.add(plane)
        handle = mock_open_fn()
        # В случае дубликата, не должно быть вызова записи
        handle.write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
