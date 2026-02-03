import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import Product, Category


def test_product_attributes():
    """Тестируем все атрибуты Product"""
    p = Product("Name", "Description", 100.0, 5)
    assert hasattr(p, 'name')
    assert hasattr(p, 'description')
    assert hasattr(p, 'price')
    assert hasattr(p, 'quantity')
    assert p.name == "Name"
    assert p.description == "Description"
    assert p.price == 100.0
    assert p.quantity == 5


def test_category_attributes():
    """Тестируем все атрибуты Category"""
    p = Product("Test", "Test", 10.0, 1)
    c = Category("Cat", "Desc", [p])

    assert hasattr(c, 'name')
    assert hasattr(c, 'description')
    assert hasattr(c, 'products')
    assert c.name == "Cat"
    assert c.description == "Desc"
    assert len(c.products) == 1


def test_class_attributes():
    """Тестируем атрибуты класса Category"""
    # Сохраняем начальные значения
    initial_categories = Category.category_count
    initial_products = Category.product_count

    # Создаём новые объекты
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    Category("NewCat", "Desc", [p1, p2])

    # Проверяем, что счётчики увеличились
    assert Category.category_count == initial_categories + 1
    assert Category.product_count == initial_products + 2


def test_empty_products_list():
    """Тестируем категорию с пустым списком товаров"""
    c = Category("Empty", "No products", [])
    assert len(c.products) == 0
    # Счётчик категорий должен увеличиться, товаров - нет