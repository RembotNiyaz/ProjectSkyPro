import pytest
from src.main import Product, Category

def test_product_initialization():
    product = Product("Телефон", "Описание", 999.99, 10)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 999.99
    assert product.quantity == 10

def test_category_initialization():
    product1 = Product("Телефон 1", "Описание 1", 500.0, 5)
    product2 = Product("Телефон 2", "Описание 2", 700.0, 3)
    category = Category("Категория телефонов", "Описание категории", [product1, product2])
    assert category.name == "Категория телефонов"
    assert category.description == "Описание категории"
    assert category.products == [product1, product2]
    # Проверка, что счетчики увеличились
    assert Category.category_count >= 1
    assert Category.product_count >= 2

def test_counts_increment():
    initial_category_count = Category.category_count
    initial_product_count = Category.product_count

    product = Product("Test Product", "Test Description", 100.0, 2)
    category = Category("Test Category", "Test Description", [product])

    assert Category.category_count == initial_category_count + 1
    assert Category.product_count == initial_product_count + 1