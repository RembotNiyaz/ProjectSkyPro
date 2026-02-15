import pytest
from src.models import Airplane, JSONFileSaver
import json

def test_add_and_get_all(tmp_path):
    file_path = tmp_path / "test_airplanes.json"
    saver = JSONFileSaver(filename=str(file_path))

    airplane1 = Airplane("XYZ789", "FR", 550, 12000)
    airplane2 = Airplane("XYZ456", "FR", 580, 13000)

    # Добавляем первое
    saver.add(airplane1)
    data = saver.get_all()
    assert isinstance(data, list)
    assert any(a["call_sign"] == "XYZ789" for a in data)

    # Добавляем второе
    saver.add(airplane2)
    data = saver.get_all()
    assert len(data) == 2

    # Проверка, что дубликат не добавляется (по call_sign)
    saver.add(airplane1)
    data_after = saver.get_all()
    assert len(data_after) == 2


def test_delete_airplane(tmp_path):
    file_path = tmp_path / "test_airplanes.json"
    saver = JSONFileSaver(filename=str(file_path))

    airplane = Airplane("DEL123", "DE", 600, 10000)
    saver.add(airplane)
    data = saver.get_all()
    assert any(a["call_sign"] == "DEL123" for a in data)

    # Удаление
    saver.delete("DEL123")
    data_after = saver.get_all()
    assert not any(a["call_sign"] == "DEL123" for a in data_after)


def test_get_all_empty_file(tmp_path):
    file_path = tmp_path / "empty.json"
    # Создаем пустой файл
    file_path.write_text("[]")
    saver = JSONFileSaver(filename=str(file_path))
    data = saver.get_all()
    assert data == []

def test_airplane_creation():
    airplane = Airplane("ABC123", "USA", 500, 10000)
    assert airplane.call_sign == "ABC123"
    assert airplane.registration_country == "USA"
    assert airplane.speed == 500
    assert airplane.altitude == 10000

def test_airplane_invalid_types():
    with pytest.raises(ValueError):
        Airplane(123, "USA", 500, 10000)
    with pytest.raises(ValueError):
        Airplane("ABC123", 456, 500, 10000)
    with pytest.raises(ValueError):
        Airplane("ABC123", "USA", "fast", 10000)
    with pytest.raises(ValueError):
        Airplane("ABC123", "USA", 500, "high")

def test_airplane_comparison():
    a1 = Airplane("A1", "RU", 600, 15000)
    a2 = Airplane("A2", "RU", 700, 15000)
    assert a1 < a2
    assert a2 > a1
    a3 = Airplane("A1", "RU", 600, 15000)
    assert a1 == a3