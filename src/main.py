from abc import ABC, abstractmethod


# Миксин, выводящий информацию при создании объекта
class CreatorInfoMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {args} {kwargs}")
        super().__init__(*args, **kwargs)


# Абстрактный базовый класс
class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self):
        pass


# Основной класс продукта
class Product(CreatorInfoMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description)
        # Задание 1: выбрасываем исключение, если количество равно нулю
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.__price = price
        self._quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price >= 0:
            if new_price < self.__price:
                answer = input(f"Вы хотите снизить цену с {self.__price} до {new_price}. Продолжить? (y/n): ").lower()
                if answer != "y":
                    print("Снижение цены отменено.")
                    return
            self.__price = new_price
        else:
            print("Цена не должна быть отрицательной или нулевой.")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self._quantity = value
        else:
            print("Количество не может быть отрицательным.")

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self._quantity} шт."

    def __add__(self, other):
        if isinstance(self, type(other)):
            total_price = self.__price * self._quantity + other.__price * other._quantity
            return total_price
        raise TypeError("Нельзя складывать объекты разных классов.")

    @classmethod
    def new_product(cls, data: dict):
        return cls(**data)


# Класс Smartphone наследует от Product
class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        base_str = super().__str__()
        return (
            f"{base_str}\n"
            f"Производительность: {self.efficiency}\n"
            f"Модель: {self.model}\n"
            f"Объем памяти: {self.memory}GB\n"
            f"Цвет: {self.color}"
        )


# Класс LawnGrass наследует от Product
class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        base_str = super().__str__()
        return (
            f"{base_str}\n"
            f"Страна-производитель: {self.country}\n"
            f"Срок прорастания: {self.germination_period}\n"
            f"Цвет: {self.color}"
        )


# Класс Category
class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = []
        self._product_count = 0
        for product in products:
            self.add_product(product)
        Category.category_count += 1

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников.")
        # Проверка на дублирование по имени
        if any(p.name == product.name for p in self.__products):
            print(f"Продукт с названием {product.name} уже есть в категории.")
            return
        self.__products.append(product)
        self._product_count += 1
        Category.product_count += 1

    @property
    def products(self):
        return "\n".join(str(p) for p in self.__products)

    @property
    def product_list(self):
        return self.__products

    def __str__(self):
        return f"Категория: {self.name}\n{self.products}"

    # Задание 2: Реализовать метод подсчета среднего ценника
    def middle_price(self):
        try:
            total = sum(p.price for p in self.__products)
            count = len(self.__products)
            if count == 0:
                return 0
            return total / count
        except ZeroDivisionError:
            # Обработка деления на ноль
            return 0


# Тестовая часть
if __name__ == "__main__":
    # Попытка создать продукт с нулевым количеством (задание 1)
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством"
        )
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    # Создаем продукты
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию с товарами
    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    # Тест метода middle_price
    print("Средний ценник товаров в категории:", category1.middle_price())

    # Создаем пустую категорию
    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print("Средний ценник в пустой категории:", category_empty.middle_price())

    # Проверка исключения при делении на ноль (у пустой категории)
    # (должен вернуть 0)

    # Дополнительно:
    # Попытка создать товар с нулевым количеством (задание 1)
    try:
        product_invalid2 = Product("Товар", "Описание", 100, 0)
    except ValueError as e:
        print("Обработка исключения для товара с нулевым количеством прошла успешно.")
