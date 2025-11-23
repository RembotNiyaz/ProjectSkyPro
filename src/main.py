class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
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
        if type(self) != type(other):
            raise TypeError("Нельзя складывать объекты разных классов.")
        total_price = self.__price * self._quantity + other.__price * other._quantity
        return total_price


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str}\n"
                f"Производительность: {self.efficiency}\n"
                f"Модель: {self.model}\n"
                f"Объем памяти: {self.memory}GB\n"
                f"Цвет: {self.color}")


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str}\n"
                f"Страна-производитель: {self.country}\n"
                f"Срок прорастания: {self.germination_period}\n"
                f"Цвет: {self.color}")


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
        # Проверка на дублирование, если нужно
        if any(p.name == product.name for p in self.__products):
            print(f"Продукт с именем {product.name} уже есть в категории.")
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


# Тестовая часть, если запустить как main
if __name__ == "__main__":
    # Создаем продукты
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1)
    print()
    print(smartphone2)
    print()
    print(smartphone3)
    print()

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1)
    print()
    print(grass2)
    print()

    # Проверка сложения
    try:
        smartphone_sum = smartphone1 + smartphone2
        print("Общая стоимость смартфонов:", smartphone_sum)
    except TypeError as e:
        print(e)

    try:
        grass_sum = grass1 + grass2
        print("Общая стоимость травы:", grass_sum)
    except TypeError as e:
        print(e)

    # Попытка сложить разные классы
    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения смартфона и травы.")

    # Создаем категории
    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    print("\nКатегории и их содержимое:")
    print(category_smartphones)
    print()
    print(category_grass)
    print()

    # Добавление продукта
    category_smartphones.add_product(smartphone3)
    print("После добавления нового смартфона:")
    print(category_smartphones)
    print()

    # Попытка добавить неподходящий объект
    try:
        category_smartphones.add_product("Не продукт")
    except TypeError as e:
        print("Ошибка при добавлении не продукта:", e)

    # Проверка счетчиков
    print("\nОбщее количество категорий:", Category.category_count)
    print("Общее количество продуктов:", Category.product_count)