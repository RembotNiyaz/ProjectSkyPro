import pytest
from unittest.mock import patch
from src.main import Product, Category

def test_product_initialization():
    product = Product("Телефон", "Описание", 999.99, 10)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 999.99  # через property
    assert product._quantity == 10

def test_category_initialization():
    product1 = Product("Телефон 1", "Описание 1", 500.0, 5)
    product2 = Product("Телефон 2", "Описание 2", 700.0, 3)
    category = Category("Категория телефонов", "Описание категории", [product1, product2])
    assert category.name == "Категория телефонов"
    assert category.description == "Описание категории"
    expected_output = (
        f"{product1.name}, {product1.price} руб. Остаток: {product1.quantity} шт.\n"
        f"{product2.name}, {product2.price} руб. Остаток: {product2.quantity} шт.\n"
    )
    assert category.products == expected_output


def test_counts_increment():
    initial_category_count = Category.category_count
    initial_product_count = Category.product_count

    product = Product("Test Product", "Test Description", 100.0, 2)
    category = Category("Test Category", "Test Description", [product])

    assert Category.category_count == initial_category_count + 1
    assert Category.product_count == initial_product_count + 1

@patch('builtins.input', return_value='y')
def test_price_reduction_confirm(mock_input):
    product = Product("Test", "desc", 100, 10)
    # Снижаем цену ниже текущей, подтверждение 'y'
    product.price = 50
    assert product.price == 50

@patch('builtins.input', return_value='n')
def test_price_reduction_cancel(mock_input):
    product = Product("Test", "desc", 100, 10)
    old_price = product.price
    # Снижаем цену ниже текущей, подтверждение 'n'
    product.price = 50
    # Цена не должна измениться
    assert product.price == old_price

def test_price_negative_value():
    product = Product("Test", "desc", 100, 10)
    product.price = -50  # Некорректное изменение
    assert product.price == 100  # Цена не должна измениться

def test_new_product_method():
    data = {
        "name": "NewProd",
        "description": "desc",
        "price": 200,
        "quantity": 5
    }
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "NewProd"
    assert product.description == "desc"
    assert product.price == 200
    assert product._quantity == 5

def test_add_product_increases_count():
    category = Category("TestCat", "desc", [])
    initial_product_count = Category.product_count
    product = Product("A", "desc", 10, 1)
    category.add_product(product)
    assert Category.product_count == initial_product_count + 1
    assert product in category._Category__products

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
    product = Product("Dup", "desc", 100, 1)
    category = Category("Cat", "desc", [product])
    category.add_product(product)
    # Проверка, что продукт не добавляется повторно или что происходит
    # В зависимости от реализации, например:
    assert category._Category__products.count(product) == 1

def test_category_with_empty_products():
    category = Category("EmptyCategory", "desc", [])
    assert category.products == ""

def test_set_negative_quantity():
    product = Product("Test", "desc", 100, 5)
    product.quantity = -3
    # Количество не должно измениться
    assert product.quantity == 5

def test_set_negative_price():
    product = Product("Test", "desc", 100, 5)
    product.price = -10
    # Цена не должна измениться
    assert product.price == 100

def test_product_str():
    product = Product("Тест", "Описание", 999.99, 5)
    expected_str = "Тест, 999.99 руб. Остаток: 5 шт."
    assert str(product) == expected_str

def test_category_str():
    p1 = Product("П1", "desc", 100, 2)
    p2 = Product("П2", "desc", 200, 3)
    category = Category("Категория", "desc", [p1, p2])
    output = str(category)
    total_quantity = p1.quantity + p2.quantity
    assert "Категория" in output
    assert f"количество продуктов: {total_quantity} шт." in output

def test_product_add():
    p1 = Product("A", "desc", 10, 3)  # 30
    p2 = Product("B", "desc", 20, 2)  # 40
    total = p1 + p2
    assert total == 70

def test_product_add_with_non_product():
    p = Product("A", "desc", 10, 3)
    result = p.__add__(123)
    assert result is NotImplemented or result is None