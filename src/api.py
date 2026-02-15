import requests
from abc import ABC, abstractmethod


class BaseAPI(ABC):
    def __init__(self):
        self._session = requests.Session()

    @abstractmethod
    def _connect(self, url: str, params: dict):
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class OpenStreetMapAPI(BaseAPI):
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def _connect(self, url: str, params: dict):
        response = self._session.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Error connecting to {url}: {response.status_code}")
        return response

    def get_country_bounding_box(self, country_name: str):
        params = {"q": country_name, "format": "json", "limit": 1}
        response = self._connect(self.BASE_URL, params)
        data = response.json()
        if not data:
            raise ValueError(f"Country {country_name} not found")
        boundingbox = data[0]["boundingbox"]
        # boundingbox: [south, north, west, east]
        return list(map(float, boundingbox))

    def get_data(self, url, params):
        response = self._connect(url, params)
        return response.json()


class OpenSkyAPI(BaseAPI):
    BASE_URL = "https://opensky-network.org/api/states/all"

    def get_airplanes_in_bbox(self, south, north, west, east):
        params = {"lamin": south, "lamax": north, "lomin": west, "lomax": east}
        response = self._connect(self.BASE_URL, params)
        data = response.json()
        return data.get("states", [])

    def _connect(self, url: str, params: dict):
        response = self._session.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Error connecting to {url}: {response.status_code}")
        return response

    def get_data(self, url, params):
        response = self._connect(url, params)
        return response.json()
