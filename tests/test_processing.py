import pytest

from src.processing import filter_by_state, sort_by_date


"""Тестовый метод для проверки фильтрации данных по состоянию (state)"""


def test_state(state_filter):
    assert filter_by_state(state_filter) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


"""Тестовый метод для проверки фильтрации данных по состоянию (state) в отсутсвие некоторых элементов списка"""


def test_state2(state_filter2):
    assert filter_by_state(state_filter2) == [
        {"state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED"},
    ]


"""Тестовый метод для проверки корректности сортировки данных по дате в порядке убывания"""


def test_data_filter(date_filter):
    assert sort_by_date(date_filter, 1) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


"""Тестовый метод для проверки корректности сортировки данных по дате в порядке возрастания"""


def test_data_filter2(date_filter):
    assert sort_by_date(date_filter, 0) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
