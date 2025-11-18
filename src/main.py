class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # приватный атрибут цены с двойным подчеркиванием
        self._quantity = quantity  # при необходимости тоже можно сделать приватным

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price >= 0:
            # Логика по снижению цены с подтверждением
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

    @classmethod
    def new_product(cls, product_dict):
        """
        Создает новый продукт из словаря.
        """
        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = []  # приватный список товаров
        self._product_count = 0  # счетчик товаров в категории
        for product in products:
            self.add_product(product)
        Category.category_count += 1

    def add_product(self, product):
        if product not in self.__products:
            self.__products.append(product)
            self._product_count += 1
            Category.product_count += 1
        else:
            print("Этот продукт уже есть в категории.")

    @property
    def products(self):
        # Форматированный вывод товаров
        return "".join(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n" for p in self.__products)


# --- Тестирование --- #
if __name__ == "__main__":
    # Создаем товары
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию и добавляем товары
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Выводим список товаров
    print(category1.products)

    # Добавляем новый товар
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    # Проверяем обновленный список товаров
    print(category1.products)

    # Количество товаров в категории
    print(f"Общее количество товаров: {category1._product_count}")

    # Создаем товар через класс-метод new_product
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )

    # Выводим информацию о новом товаре
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # Проверка изменения цены
    new_product.price = 800
    print(f"Обновленная цена: {new_product.price}")

    # Попытка снизить цену до отрицательного значения
    new_product.price = -100
    print(f"После попытки установить отрицательную цену: {new_product.price}")

    # Установка цены равной нулю (должна пройти)
    new_product.price = 0
    print(f"Цена после установки нуля: {new_product.price}")

    # Проверка изменения количества
    print(f"Исходное количество: {new_product.quantity}")
    new_product.quantity = 10
    print(f"Обновленное количество: {new_product.quantity}")
    # Попытка установить отрицательное количество
    new_product.quantity = -3
    print(f"После попытки установить отрицательное количество: {new_product.quantity}")