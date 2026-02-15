from src.api import OpenStreetMapAPI, OpenSkyAPI
from src.models import Airplane
from src.file_savers import JSONFileSaver
from src.utils import filter_by_country, get_top_n


def user_interaction():
    country_name = input("Введите название страны: ")
    top_n = int(input("Введите количество самолетов для топ N: "))
    filter_countries = input("Введите через запятую страны регистрации для фильтрации: ").split(",")

    # Получение координат страны
    osm_api = OpenStreetMapAPI()
    south, north, west, east = osm_api.get_country_bounding_box(country_name)

    # Получение данных о самолетах
    os_api = OpenSkyAPI()
    states = os_api.get_airplanes_in_bbox(south, north, west, east)

    # Преобразование в объекты
    airplanes = []
    for state in states:
        call_sign = state[1]
        registration_country = state[2]
        speed = state[9] if state[9] is not None else 0
        altitude = state[13] if state[13] is not None else 0
        airplanes.append(Airplane(call_sign, registration_country, speed, altitude))

    # Фильтрация по странам
    filtered_planes = filter_by_country(airplanes, [c.strip() for c in filter_countries])
    # Топ N по высоте
    top_planes = get_top_n(filtered_planes, top_n)

    # Вывод результата
    for plane in top_planes:
        print(plane)

    # Сохранение в файл
    saver = JSONFileSaver()
    for plane in top_planes:
        saver.add(plane)


if __name__ == "__main__":
    user_interaction()
