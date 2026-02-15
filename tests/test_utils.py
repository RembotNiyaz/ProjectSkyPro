import pytest
from src.utils import filter_by_country, get_top_n, get_airplanes_in_altitude_range, sort_by_altitude
from src.models import Airplane

# Создадим фикстуру с тестовыми объектами
@pytest.fixture
def sample_airplanes():
    return [
        Airplane(call_sign="A1", registration_country="USA", speed=500, altitude=10000),
        Airplane(call_sign="A2", registration_country="Germany", speed=600, altitude=20000),
        Airplane(call_sign="A3", registration_country="USA", speed=550, altitude=15000),
        Airplane(call_sign="A4", registration_country="France", speed=450, altitude=5000),
        Airplane(call_sign="A5", registration_country="Germany", speed=700, altitude=25000),
    ]

def test_filter_by_country(sample_airplanes):
    # Отфильтруем по странам "USA" и "Germany"
    result = filter_by_country(sample_airplanes, ["USA", "Germany"])
    # Проверяем, что все в результате из указанных стран
    for plane in result:
        assert plane.registration_country in ["USA", "Germany"]
    # Количество должно быть 4
    assert len(result) == 4

def test_get_top_n(sample_airplanes):
    # Получим топ 2 по высоте
    top_planes = get_top_n(sample_airplanes, 2)
    # Проверяем, что в результате 2 элемента
    assert len(top_planes) == 2
    # Они должны быть с максимальными высотами
    assert top_planes[0].altitude >= top_planes[1].altitude
    # Проверяем правильность сортировки высот
    assert top_planes[0].altitude == 25000
    assert top_planes[1].altitude == 20000


def test_sort_by_altitude(sample_airplanes):
    sorted_planes = sort_by_altitude(sample_airplanes)
    # Проверяем, что высоты идут по убыванию
    for i in range(len(sorted_planes) - 1):
        assert sorted_planes[i].altitude >= sorted_planes[i+1].altitude
    # Первая должна быть с максимальной высотой
    assert sorted_planes[0].altitude == 25000
    # Последняя с минимальной высотой
    assert sorted_planes[-1].altitude == 5000