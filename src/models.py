from abc import ABC, abstractmethod


class Airplane:
    __slots__ = ["call_sign", "registration_country", "speed", "altitude", "other_attributes"]

    def __init__(self, call_sign: str, registration_country: str, speed: float, altitude: float, **kwargs):
        self.call_sign = call_sign
        self.registration_country = registration_country
        self.speed = speed
        self.altitude = altitude
        self.other_attributes = kwargs
        self._validate()

    def _validate(self):
        if not isinstance(self.call_sign, str):
            raise ValueError("call_sign must be a string")
        if not isinstance(self.registration_country, str):
            raise ValueError("registration_country must be a string")
        if not isinstance(self.speed, (int, float)):
            raise ValueError("speed must be a number")
        if not isinstance(self.altitude, (int, float)):
            raise ValueError("altitude must be a number")
        # дополнительные проверки по необходимости

    def __repr__(self):
        return (
            f"Airplane(call_sign={self.call_sign}, country={self.registration_country}, "
            f"speed={self.speed}, altitude={self.altitude})"
        )

    def __lt__(self, other):
        if not isinstance(other, Airplane):
            return NotImplemented
        return self.speed < other.speed

    def __gt__(self, other):
        if not isinstance(other, Airplane):
            return NotImplemented
        return self.speed > other.speed

    def __eq__(self, other):
        if not isinstance(other, Airplane):
            return NotImplemented
        return self.call_sign == other.call_sign

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            call_sign=data["call_sign"],
            registration_country=data["registration_country"],
            speed=data["speed"],
            altitude=data["altitude"],
        )

    def to_dict(self):
        return {
            "call_sign": self.call_sign,
            "registration_country": self.registration_country,
            "speed": self.speed,
            "altitude": self.altitude,
        }


class AbstractFileSaver(ABC):
    @abstractmethod
    def add(self, airplane: Airplane):
        pass

    @abstractmethod
    def delete(self, call_sign: str):
        pass

    @abstractmethod
    def get_all(self):
        pass


class JSONFileSaver(AbstractFileSaver):
    def __init__(self, filename="airplanes.json"):
        import os

        self.__filename = filename
        # создаем файл, если не существует
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w") as f:
                f.write("[]")

    def add(self, airplane: Airplane):
        import json

        data = self.get_all()
        # проверка на дубли
        if any(a["call_sign"] == airplane.call_sign for a in data):
            return  # или обновление
        data.append(airplane.to_dict())
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self, call_sign: str):
        import json

        data = self.get_all()
        data = [a for a in data if a["call_sign"] != call_sign]
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        import json

        with open(self.__filename, "r") as f:
            return json.load(f)
