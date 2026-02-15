from models import Airplane


def filter_by_country(airplanes, country_list):
    return [a for a in airplanes if a.registration_country in country_list]


def get_top_n(airplanes, n):
    sorted_planes = sorted(airplanes, key=lambda a: a.altitude, reverse=True)
    return sorted_planes[:n]


def get_airplanes_in_altitude_range(airplanes, min_alt, max_alt):
    return [a for a in airplanes if min_alt <= a.altitude <= max_alt]


def sort_by_altitude(airplanes):
    return sorted(airplanes, key=lambda a: a.altitude, reverse=True)
