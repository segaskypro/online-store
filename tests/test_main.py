# tests/test_main.py
import os
import sys

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import Product, Category


class TestProduct:
    """Тесты для класса Product"""

    def test_product_creation(self):
        """Проверяем, что товар создаётся с правильными значениями"""
        product = Product("Телевизор", "4K, 55 дюймов", 50000.0, 3)

        assert product.name == "Телевизор"
        assert product.description == "4K, 55 дюймов"
        assert product.price == 50000.0
        assert product.quantity == 3

    def test_product_default_values(self):
        """Проверяем создание товара с нулевым количеством"""
        product = Product("Книга", "Художественная литература", 500.0, 0)
        assert product.quantity == 0


class TestCategory:
    """Тесты для класса Category"""

    def test_category_creation(self):
        """Проверяем создание категории"""
        # Создаём тестовые товары
        product1 = Product("Мышь", "Беспроводная", 1500.0, 10)
        product2 = Product("Клавиатура", "Механическая", 5000.0, 5)

        # Создаём категорию
        category = Category(
            "Компьютерная периферия",
            "Устройства ввода",
            [product1, product2]
        )

        assert category.name == "Компьютерная периферия"
        assert category.description == "Устройства ввода"
        assert len(category.products) == 2
        # Проверяем, что в списке действительно объекты Product
        assert isinstance(category.products[0], Product)
        assert isinstance(category.products[1], Product)

    def test_category_count(self):
        """Проверяем подсчёт количества категорий"""
        # Запоминаем текущее количество
        initial_count = Category.category_count

        # Создаём новую категорию
        product = Product("Тест", "Тест", 100.0, 1)
        category = Category("Тестовая категория", "Для теста", [product])

        # Проверяем, что счётчик увеличился на 1
        assert Category.category_count == initial_count + 1

    def test_product_count(self):
        """Проверяем подсчёт общего количества товаров"""
        # Запоминаем текущее количество товаров
        initial_count = Category.product_count

        # Создаём товары
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)
        product3 = Product("Товар 3", "Описание 3", 300.0, 1)

        # Создаём категорию с 3 товарами
        category = Category("Категория", "Описание", [product1, product2, product3])

        # Проверяем, что счётчик увеличился на 3
        assert Category.product_count == initial_count + 3

    def test_empty_category(self):
        """Проверяем создание пустой категории (без товаров)"""
        category = Category("Пустая категория", "Нет товаров", [])

        assert category.name == "Пустая категория"
        assert len(category.products) == 0
        # Счётчик категорий должен увеличиться, а товаров - нет
        # В tests/test_main.py добавь в конец:
        def test_main_function():
            """Тестируем основную функцию"""
            from main import main

            # Можно проверить, что функция существует и вызывается
            assert callable(main)

            # Или проверить вывод (более сложно)
            import io
            import sys

            # Сохраняем оригинальный stdout
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            try:
                main()
                output = buffer.getvalue()
                assert "Категория: Смартфоны" in output
                assert "Всего категорий: 1" in output
            finally:
                sys.stdout = old_stdout
