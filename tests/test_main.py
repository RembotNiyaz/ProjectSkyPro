import pytest
from unittest.mock import patch
from src.main import Product, Category, Smartphone, LawnGrass, BaseProduct


def test_product_initialization():
    product = Product("Телефон", "Описание", 999.99, 10)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 999.99
    assert product._quantity == 10


def test_counts_increment():
    initial_category_count = Category.category_count
    initial_product_count = Category.product_count

    product = Product("Test Product", "Test Description", 100.0, 2)
    category = Category("Test Category", "Test Description", [product])

    assert Category.category_count == initial_category_count + 1
    assert Category.product_count == initial_product_count + 1


@patch("builtins.input", return_value="y")
def test_price_reduction_confirm(mock_input):
    product = Product("Test", "desc", 100, 10)
    product.price = 50
    assert product.price == 50


@patch("builtins.input", return_value="n")
def test_price_reduction_cancel(mock_input):
    product = Product("Test", "desc", 100, 10)
    old_price = product.price
    product.price = 50
    assert product.price == old_price


def test_price_negative_value():
    product = Product("Test", "desc", 100, 10)
    product.price = -50
    assert product.price == 100  # Цена не должна измениться


def test_new_product_method():

    data = {"name": "NewProd", "description": "desc", "price": 200, "quantity": 5}
    product = Product(**data)

    # если метода staticmethod нет, создавайте напрямую
    data = {"name": "NewProd", "description": "desc", "price": 200, "quantity": 5}
    product = Product(**data)  # или Product.new_product(data), если есть

    assert isinstance(product, Product)
    assert product.name == "NewProd"


def test_add_duplicate_product():
    product = Product("Dup", "desc", 100, 1)
    category = Category("Cat", "desc", [product])
    initial_count = len(category._Category__products)
    category.add_product(product)
    assert len(category._Category__products) == initial_count


def test_products_property():
    product1 = Product("A", "desc", 10, 1)
    product2 = Product("B", "desc", 20, 2)
    category = Category("Test", "desc", [product1, product2])
    output = category.products
    assert "A" in output
    assert "B" in output
    assert "10 руб" in output
    assert "20 руб" in output


def test_add_duplicate_product():
    category = Category("Test", "desc", [])
    product = Product("Item", "desc", 100, 1)
    category.add_product(product)
    category.add_product(product)  # дубли
    assert len(category.product_list) == 1


def test_category_with_empty_products():
    category = Category("EmptyCategory", "desc", [])
    assert category.products == ""


def test_set_negative_quantity():
    product = Product("Test", "desc", 100, 5)
    product.quantity = -3
    assert product.quantity == 5


def test_set_negative_price():
    product = Product("Test", "desc", 100, 5)
    product.price = -10
    assert product.price == 100


def test_increase_price():
    product = Product("Test", "desc", 100, 10)
    product.price = 150
    assert product.price == 150


@patch("builtins.input", return_value="y")
def test_price_increase_with_confirmation(mock_input):
    product = Product("Test", "desc", 100, 10)
    product.price = 120
    assert product.price == 120


def test_add_multiple_same_products():
    product = Product("Same", "desc", 50, 2)
    category = Category("Test", "desc", [])
    category.add_product(product)
    category.add_product(product)
    assert len(category.product_list) == 1


def test_category_str_contains_name_and_products():
    product = Product("Item", "desc", 100, 1)
    category = Category("MyCategory", "desc", [product])
    output = str(category)
    assert "MyCategory" in output
    assert "Item" in output


def test_add_product_raises_type_error():
    category = Category("Test", "desc", [])
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_product_list_is_list_of_products():
    product1 = Product("A", "desc", 10, 1)
    product2 = Product("B", "desc", 20, 2)
    category = Category("Test", "desc", [product1, product2])
    plist = category.product_list
    assert isinstance(plist, list)
    assert all(isinstance(p, Product) for p in plist)


def test_change_quantity():
    product = Product("Test", "desc", 100, 5)
    product.quantity = 10
    assert product.quantity == 10
    product.quantity = -3
    assert product.quantity == 10


def test_str_representation_of_product():
    product = Product("Test", "desc", 100, 5)
    s = str(product)
    assert "Test" in s
    assert "100 руб" in s
    assert "Остаток" in s


# Новые тесты для новых классов и миксина
def test_baseproduct_is_abstract():
    import abc

    with pytest.raises(TypeError):
        BaseProduct()


def test_product_inherits_from_baseproduct():
    product = Product("Test", "desc", 50, 1)
    assert isinstance(product, BaseProduct)


def test_smartphone_str():
    sp = Smartphone("Phone", "desc", 1000, 3, 80.5, "ModelX", 128, "Red")
    s_str = str(sp)
    assert "Производительность" in s_str
    assert "Модель" in s_str
    assert "Объем памяти" in s_str


def test_lawn_grass_str():
    grass = LawnGrass("Grass", "desc", 50, 10, "USA", "5 days", "Green")
    s_str = str(grass)
    assert "Страна-производитель" in s_str
    assert "Срок прорастания" in s_str


def test_creator_info_mixin_print(capsys):
    # Создадим объект и проверим, что выводится сообщение
    product = Product("Test", "desc", 100, 1)
    captured = capsys.readouterr()
    assert "Создан объект класса Product" in captured.out
    # Аналогично для Smartphone
    smartphone = Smartphone("Smart", "desc", 500, 2, 90, "ModelY", 64, "Blue")
    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone" in captured.out
    # Для LawnGrass
    grass = LawnGrass("Grass", "desc", 30, 5, "Canada", "7 days", "Dark Green")
    captured = capsys.readouterr()
    assert "Создан объект класса LawnGrass" in captured.out


def test_add_product_increases_count():
    category = Category("TestCat", "desc", [])
    initial_product_count = Category.product_count
    product = Product("A", "desc", 10, 1)
    category.add_product(product)
    assert Category.product_count == initial_product_count + 1
    assert product in category._Category__products


def test_product_str():
    product = Product("Тест", "Описание", 999.99, 5)
    expected_str = "Тест, 999.99 руб. Остаток: 5 шт."
    assert str(product) == expected_str


def test_product_add():
    p1 = Product("A", "desc", 10, 3)  # 30
    p2 = Product("B", "desc", 20, 2)  # 40
    total = p1 + p2
    assert total == 70

def test_middle_price_empty_category():
    empty_category = Category("Empty", "desc", [])
    assert empty_category.middle_price() == 0

def test_middle_price_with_products():
    p1 = Product("A", "desc", 100, 2)  # цена 100
    p2 = Product("B", "desc", 200, 3)  # цена 200
    cat = Category("TestCat", "desc", [p1, p2])
    expected = (100 + 200) / 2  # 150.0
    assert cat.middle_price() == expected