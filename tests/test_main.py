# tests/test_main.py
import os
import sys
import pytest

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


# ========== НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 2 ==========

class TestProductStr:
    """Тесты для магического метода __str__ класса Product"""

    def test_product_str_format(self):
        """Проверяем формат строки продукта"""
        product = Product("Тестовый продукт", "Тестовое описание", 100.0, 10)
        expected = "Тестовый продукт, 100.0 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_product_str_with_different_values(self):
        """Проверяем строковое представление с другими значениями"""
        product = Product("iPhone", "Смартфон", 80000.0, 3)
        expected = "iPhone, 80000.0 руб. Остаток: 3 шт."
        assert str(product) == expected

    def test_product_str_zero_quantity(self):
        """Проверяем продукт с нулевым количеством"""
        product = Product("Пустой товар", "Нет в наличии", 100.0, 0)
        expected = "Пустой товар, 100.0 руб. Остаток: 0 шт."
        assert str(product) == expected

    def test_product_str_float_price(self):
        """Проверяем продукт с ценой в виде float"""
        product = Product("Товар", "Описание", 99.99, 5)
        expected = "Товар, 99.99 руб. Остаток: 5 шт."
        assert str(product) == expected


class TestCategoryStr:
    """Тесты для магического метода __str__ класса Category"""

    def test_category_str_format(self):
        """Проверяем формат строки категории с несколькими товарами"""
        product1 = Product("Товар 1", "Описание 1", 50.0, 5)
        product2 = Product("Товар 2", "Описание 2", 150.0, 3)
        product3 = Product("Товар 3", "Описание 3", 200.0, 10)
        category = Category("Тестовая категория", "Описание", [product1, product2, product3])

        # Сумма количеств: 5 + 3 + 10 = 18
        expected = "Тестовая категория, количество продуктов: 18 шт."
        assert str(category) == expected

    def test_category_str_empty_products(self):
        """Проверяем категорию без товаров"""
        category = Category("Пустая категория", "Нет товаров", [])
        expected = "Пустая категория, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_str_single_product(self):
        """Проверяем категорию с одним товаром"""
        product = Product("Один товар", "Описание", 100.0, 7)
        category = Category("Категория с одним товаром", "Описание", [product])
        expected = "Категория с одним товаром, количество продуктов: 7 шт."
        assert str(category) == expected

    def test_category_str_large_quantities(self):
        """Проверяем категорию с большими количествами"""
        product1 = Product("Товар 1", "Описание", 100.0, 1000)
        product2 = Product("Товар 2", "Описание", 200.0, 500)
        category = Category("Крупная категория", "Описание", [product1, product2])

        expected = "Крупная категория, количество продуктов: 1500 шт."
        assert str(category) == expected


class TestProductAdd:
    """Тесты для магического метода __add__ класса Product"""

    def test_product_add_two_products(self):
        """Проверяем сложение двух продуктов"""
        product1 = Product("Товар A", "Описание A", 100.0, 10)
        product2 = Product("Товар B", "Описание B", 200.0, 2)

        # Ожидаем: 100*10 + 200*2 = 1000 + 400 = 1400
        expected = 1400.0
        assert product1 + product2 == expected

    def test_product_add_with_zero_quantity(self):
        """Проверяем сложение с продуктом, у которого нет остатка"""
        product1 = Product("Товар A", "Описание A", 100.0, 10)
        product2 = Product("Товар B", "Описание B", 200.0, 0)

        # Ожидаем: 100*10 + 200*0 = 1000 + 0 = 1000
        expected = 1000.0
        assert product1 + product2 == expected

    def test_product_add_commutative(self):
        """Проверяем, что сложение коммутативно (a + b = b + a)"""
        product1 = Product("Товар A", "Описание A", 150.0, 4)
        product2 = Product("Товар B", "Описание B", 300.0, 1)

        assert product1 + product2 == product2 + product1

    def test_product_add_with_self(self):
        """Проверяем сложение продукта с самим собой"""
        product = Product("Товар", "Описание", 200.0, 3)
        # 200*3 + 200*3 = 600 + 600 = 1200
        expected = 1200.0
        assert product + product == expected

    def test_product_add_multiple_times(self):
        """Проверяем сложение трёх продуктов (сумма всех стоимостей)"""
        product1 = Product("Товар 1", "Описание", 100.0, 2)  # 200
        product2 = Product("Товар 2", "Описание", 200.0, 3)  # 600
        product3 = Product("Товар 3", "Описание", 300.0, 1)  # 300

        # Складываем два, потом прибавляем третий к результату
        sum12 = product1 + product2  # 200 + 600 = 800
        total = sum12 + (product3.price * product3.quantity)  # 800 + 300 = 1100

        expected = 1100.0
        assert total == expected

        # Альтернативный способ: посчитать вручную
        manual_total = (product1.price * product1.quantity) + \
                       (product2.price * product2.quantity) + \
                       (product3.price * product3.quantity)
        assert manual_total == expected

    def test_product_add_with_negative_price_product(self):
        """Проверяем сложение с продуктом, у которого отрицательная цена (должна быть 0)"""
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()  # Подавляем вывод сообщения об ошибке

        try:
            product1 = Product("Товар A", "Описание", 100.0, 5)
            product2 = Product("Товар B", "Описание", -50.0, 2)  # Цена станет 0

            # 100*5 + 0*2 = 500 + 0 = 500
            expected = 500.0
            assert product1 + product2 == expected
        finally:
            sys.stdout = old_stdout

    def test_product_add_wrong_type(self):
        """Проверяем, что при сложении с числом возникает ошибка"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError) as exc_info:
            result = product + 100
        assert "Можно складывать только объекты Product" in str(exc_info.value)

    def test_product_add_wrong_type_string(self):
        """Проверяем, что при сложении со строкой возникает ошибка"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError) as exc_info:
            result = product + "строка"
        assert "Можно складывать только объекты Product" in str(exc_info.value)

    def test_product_add_wrong_type_none(self):
        """Проверяем, что при сложении с None возникает ошибка"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError) as exc_info:
            result = product + None
        assert "Можно складывать только объекты Product" in str(exc_info.value)


class TestProductsGetterWithStr:
    """Тесты для геттера products, который теперь использует __str__"""

    def test_products_getter_uses_str_method(self):
        """Проверяем, что геттер products использует __str__ продуктов"""
        product = Product("Тестовый товар", "Описание", 1234.5, 7)
        category = Category("Категория", "Описание", [product])

        # Получаем вывод через геттер
        output = category.products

        # Проверяем, что вывод совпадает с str(product) + перевод строки
        expected = str(product) + "\n"
        assert output == expected

    def test_products_getter_multiple_products(self):
        """Проверяем геттер products с несколькими продуктами"""
        product1 = Product("Товар 1", "Описание", 100.0, 2)
        product2 = Product("Товар 2", "Описание", 200.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        output = category.products

        # Ожидаем: str(product1) + "\n" + str(product2) + "\n"
        expected = str(product1) + "\n" + str(product2) + "\n"
        assert output == expected

    def test_products_getter_with_added_product(self):
        """Проверяем, что после add_product новый продукт правильно отображается"""
        category = Category("Категория", "Описание", [])
        product = Product("Новый товар", "Описание", 300.0, 4)

        category.add_product(product)

        # Проверяем, что новый продукт отображается через __str__
        expected = str(product) + "\n"
        assert category.products == expected
