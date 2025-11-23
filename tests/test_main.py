import pytest
from unittest.mock import patch
from src.main import Product, Category

def test_product_initialization():
    product = Product("Телефон", "Описание", 999.99, 10)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 999.99  # через property
    assert product._quantity == 10


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
    # если метода staticmethod нет, создавайте напрямую
    data = {
        "name": "NewProd",
        "description": "desc",
        "price": 200,
        "quantity": 5
    }
    product = Product(**data)  # или Product.new_product(data), если есть
    assert isinstance(product, Product)
    assert product.name == "NewProd"


def test_add_duplicate_product():
    product = Product("Dup", "desc", 100, 1)
    category = Category("Cat", "desc", [product])
    initial_count = len(category._Category__products)
    category.add_product(product)
    # если добавление повторных объектов не запрещено, то длина увеличится
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
    category.add_product(product)  # добавляем дубликат
    assert len(category.product_list) == 1

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

def test_increase_price():
    product = Product("Test", "desc", 100, 10)
    product.price = 150
    assert product.price == 150

@patch('builtins.input', return_value='y')
def test_price_increase_with_confirmation(mock_input):
    product = Product("Test", "desc", 100, 10)
    product.price = 120
    assert product.price == 120

def test_add_multiple_same_products():
    product = Product("Same", "desc", 50, 2)
    category = Category("Test", "desc", [])
    category.add_product(product)
    category.add_product(product)  # Дублирование
    # количество не увеличится, так как дубликаты не добавляются
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
    # Количество не изменится
    assert product.quantity == 10

def test_str_representation_of_product():
    product = Product("Test", "desc", 100, 5)
    s = str(product)
    assert "Test" in s
    assert "100 руб" in s
    assert "Остаток" in s