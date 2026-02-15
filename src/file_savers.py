import json
from abc import ABC, abstractmethod
import os


class AbstractFileSaver(ABC):
    @abstractmethod
    def add(self, airplane):
        """Добавляет самолет в файл"""
        pass

    @abstractmethod
    def delete(self, call_sign):
        """Удаляет самолет по call_sign"""
        pass

    @abstractmethod
    def get_all(self):
        """Возвращает список всех самолетов из файла"""
        pass


class JSONFileSaver(AbstractFileSaver):
    def __init__(self, filename="airplanes.json"):
        self.__filename = filename
        # Проверка существования файла, создание если отсутствует
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w") as f:
                json.dump([], f)

    def add(self, airplane):
        data = self.get_all()
        # Проверка дублирующихся call_sign
        if any(a["call_sign"] == airplane.call_sign for a in data):
            return  # Можно обновлять, если нужно
        data.append(airplane.to_dict())
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self, call_sign):
        data = self.get_all()
        data = [a for a in data if a["call_sign"] != call_sign]
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        with open(self.__filename, "r") as f:
            return json.load(f)
