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
        # Теперь products - это геттер, возвращающий строку
        products_output = category.products
        assert isinstance(products_output, str)
        # Проверяем, что оба товара есть в выводе
        assert "Мышь" in products_output
        assert "Клавиатура" in products_output

    def test_category_count(self):
        """Проверяем подсчёт количества категорий"""
        # Запоминаем текущее количество
        initial_count = Category.category_count

        # Создаём новую категорию
        product = Product("Тест", "Тест", 100.0, 1)
        category = Category("Тестовая категория", "Для теста", [product])

        # Проверяем, что счётчик увеличился на 1
        assert Category.category_count == initial_count + 1
        # Очищаем, чтобы не влиять на другие тесты
        del category

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
        # Очищаем
        del category

    def test_empty_category(self):
        """Проверяем создание пустой категории (без товаров)"""
        category = Category("Пустая категория", "Нет товаров", [])

        assert category.name == "Пустая категория"
        assert category.products == ""  # Пустая категория - пустая строка
        # Очищаем
        del category

    def test_private_products_attribute(self):
        """Проверяем, что products - приватный атрибут"""
        product = Product("Тест", "Тест", 100.0, 1)
        category = Category("Тест", "Тест", [product])

        # Проверяем, что нельзя обратиться напрямую
        # Должен быть атрибут __products, но не products
        assert hasattr(category, '_Category__products')
        # products - это геттер, а не атрибут
        # Проверяем, что это property
        assert isinstance(type(category).products, property)

    def test_add_product_method(self):
        """Проверяем метод add_product"""
        product1 = Product("Товар 1", "Описание", 100.0, 2)
        product2 = Product("Товар 2", "Описание", 200.0, 3)

        category = Category("Категория", "Описание", [product1])
        initial_count = Category.product_count

        category.add_product(product2)

        # Проверяем, что товар добавился в вывод
        assert "Товар 2" in category.products
        # Проверяем, что счетчик увеличился
        assert Category.product_count == initial_count + 1

    def test_products_getter_format(self):
        """Проверяем формат вывода геттера products"""
        product = Product("Тестовый товар", "Описание", 1234.5, 7)
        category = Category("Категория", "Описание", [product])

        output = category.products
        # Проверяем формат: "Название, цена руб. Остаток: количество шт."
        expected = "Тестовый товар, 1234.5 руб. Остаток: 7 шт.\n"
        assert output == expected

    def test_new_product_classmethod(self):
        """Проверяем класс-метод new_product"""
        product_data = {
            'name': 'Новый товар',
            'description': 'Описание нового товара',
            'price': 999.99,
            'quantity': 5
        }

        product = Product.new_product(product_data)

        assert product.name == 'Новый товар'
        assert product.description == 'Описание нового товара'
        assert product.price == 999.99
        assert product.quantity == 5
        assert isinstance(product, Product)

    def test_price_getter_setter(self):
        """Проверяем геттер и сеттер для цены"""
        product = Product("Тест", "Тест", 100.0, 1)

        # Проверяем геттер
        assert product.price == 100.0

        # Проверяем корректную установку цены
        product.price = 150.0
        assert product.price == 150.0

        # Проверяем, что цена приватная
        assert hasattr(product, '_Product__price')

    def test_price_validation(self):
        """Проверяем валидацию цены в сеттере"""
        product = Product("Тест", "Тест", 100.0, 1)

        # Запоминаем исходную цену
        original_price = product.price

        # Пробуем установить нулевую цену
        # Нужно проверить, что цена не изменилась
        product.price = 0
        assert product.price == original_price  # Цена не должна измениться

        # Пробуем установить отрицательную цену
        product.price = -50.0
        assert product.price == original_price  # Цена не должна измениться


def test_main_function():
    """Тестируем основную функцию main()"""
    from main import main
    import io
    import sys

    # Проверяем, что функция существует
    assert callable(main)

    # Перехватываем вывод
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        # Запускаем main()
        main()
        output = buffer.getvalue()

        # Проверяем ключевые элементы вывода (не точные значения, а наличие)
        assert "Категория: Смартфоны" in output
        assert "Всего категорий:" in output  # Не проверяем точное число
        assert "Всего товаров:" in output  # Не проверяем точное число
        assert "Samsung Galaxy S23" in output
        assert "iPhone 15" in output
        assert "Xiaomi Redmi Note 13" in output
        assert "Цена не должна быть нулевая или отрицательная" in output
    finally:
        sys.stdout = old_stdout

def test_product_with_negative_price():
    """Тестируем создание продукта с отрицательной ценой"""
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        # Пытаемся создать товар с отрицательной ценой
        # Сообщение должно вывестись
        product = Product("Тест", "Тест", -100.0, 1)
        output = buffer.getvalue()
        assert "Цена не должна быть нулевая или отрицательная" in output
        # Цена должна быть 0.0 (значение по умолчанию)
        assert product.price == 0.0
    finally:
        sys.stdout = old_stdout


def test_product_with_zero_price():
    """Тестируем создание продукта с нулевой ценой"""
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        # Пытаемся создать товар с нулевой ценой
        product = Product("Тест", "Тест", 0.0, 1)
        output = buffer.getvalue()
        assert "Цена не должна быть нулевая или отрицательная" in output
        # Цена должна быть 0.0 (значение по умолчанию)
        assert product.price == 0.0
    finally:
        sys.stdout = old_stdout