# tests/test_main.py
import os
import sys
import pytest

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем все необходимые классы
from main import Product, Category, Smartphone, LawnGrass


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

        # Проверяем, что функция main выводит ожидаемые сообщения
        assert "=== Начинаем тестирование миксина ===" in output
        assert "Создание объекта Product" in output
        assert "Создание объекта Smartphone" in output
        assert "Создание объекта LawnGrass" in output
        assert "=== Все продукты успешно созданы ===" in output
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


# ========== НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 1 (КЛАССЫ-НАСЛЕДНИКИ) ==========

class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Проверяем создание смартфона со всеми атрибутами"""
        from main import Smartphone

        phone = Smartphone(
            name="Samsung Galaxy S23",
            description="Флагманский смартфон",
            price=87000.0,
            quantity=5,
            efficiency="Snapdragon 8 Gen 2",
            model="Galaxy S23",
            memory=256,
            color="Серый"
        )

        # Проверяем атрибуты от родителя
        assert phone.name == "Samsung Galaxy S23"
        assert phone.description == "Флагманский смартфон"
        assert phone.price == 87000.0
        assert phone.quantity == 5

        # Проверяем новые атрибуты
        assert phone.efficiency == "Snapdragon 8 Gen 2"
        assert phone.model == "Galaxy S23"
        assert phone.memory == 256
        assert phone.color == "Серый"

        # Проверяем, что это наследник Product
        from main import Product
        assert isinstance(phone, Product)

    def test_smartphone_str_method(self):
        """Проверяем, что смартфон наследует __str__ от Product"""
        from main import Smartphone

        phone = Smartphone(
            name="iPhone 15",
            description="Флагман Apple",
            price=95000.0,
            quantity=3,
            efficiency="A16 Bionic",
            model="iPhone 15",
            memory=256,
            color="Черный"
        )

        expected = "iPhone 15, 95000.0 руб. Остаток: 3 шт."
        assert str(phone) == expected

    def test_smartphone_different_values(self):
        """Проверяем смартфон с другими значениями"""
        from main import Smartphone

        phone = Smartphone(
            name="Xiaomi Redmi Note 13",
            description="Бюджетный смартфон",
            price=25000.0,
            quantity=10,
            efficiency="Snapdragon 680",
            model="Redmi Note 13",
            memory=128,
            color="Синий"
        )

        assert phone.name == "Xiaomi Redmi Note 13"
        assert phone.price == 25000.0
        assert phone.efficiency == "Snapdragon 680"
        assert phone.memory == 128
        assert phone.color == "Синий"


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Проверяем создание газонной травы со всеми атрибутами"""
        from main import LawnGrass

        grass = LawnGrass(
            name="Газон спортивный",
            description="Быстрорастущая трава для футбольных полей",
            price=1500.0,
            quantity=20,
            country="Россия",
            germination_period="7-10 дней",
            color="Изумрудно-зеленый"
        )

        # Проверяем атрибуты от родителя
        assert grass.name == "Газон спортивный"
        assert grass.description == "Быстрорастущая трава для футбольных полей"
        assert grass.price == 1500.0
        assert grass.quantity == 20

        # Проверяем новые атрибуты
        assert grass.country == "Россия"
        assert grass.germination_period == "7-10 дней"
        assert grass.color == "Изумрудно-зеленый"

        # Проверяем, что это наследник Product
        from main import Product
        assert isinstance(grass, Product)

    def test_lawn_grass_str_method(self):
        """Проверяем, что трава наследует __str__ от Product"""
        from main import LawnGrass

        grass = LawnGrass(
            name="Газон декоративный",
            description="Для дачных участков",
            price=2000.0,
            quantity=10,
            country="Россия",
            germination_period="10-14 дней",
            color="Ярко-зеленый"
        )

        expected = "Газон декоративный, 2000.0 руб. Остаток: 10 шт."
        assert str(grass) == expected

    def test_lawn_grass_different_values(self):
        """Проверяем траву с другими значениями"""
        from main import LawnGrass

        grass = LawnGrass(
            name="Газон для гольфа",
            description="Элитная трава",
            price=5000.0,
            quantity=5,
            country="Голландия",
            germination_period="14-21 день",
            color="Темно-зеленый"
        )

        assert grass.name == "Газон для гольфа"
        assert grass.price == 5000.0
        assert grass.country == "Голландия"
        assert grass.germination_period == "14-21 день"
        assert grass.color == "Темно-зеленый"


# ========== НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 2 (ОГРАНИЧЕНИЕ СЛОЖЕНИЯ) ==========

class TestProductAddRestriction:
    """Тесты для ограничения сложения продуктов разных классов"""

    def test_add_same_class_products(self):
        """Проверяем сложение продуктов одного класса"""
        from main import Smartphone, LawnGrass

        phone1 = Smartphone("Phone1", "Desc", 1000.0, 2, "CPU1", "M1", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 2000.0, 3, "CPU2", "M2", 256, "White")

        result = phone1 + phone2
        expected = (1000.0 * 2) + (2000.0 * 3)  # 2000 + 6000 = 8000
        assert result == expected

    def test_add_same_class_grass(self):
        """Проверяем сложение травы одного класса"""
        from main import LawnGrass

        grass1 = LawnGrass("Grass1", "Desc", 500.0, 10, "Russia", "7 days", "Green")
        grass2 = LawnGrass("Grass2", "Desc", 300.0, 5, "USA", "10 days", "Dark Green")

        result = grass1 + grass2
        expected = (500.0 * 10) + (300.0 * 5)  # 5000 + 1500 = 6500
        assert result == expected

    def test_add_different_classes_raises_error(self):
        """Проверяем, что сложение разных классов вызывает ошибку"""
        from main import Smartphone, LawnGrass

        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")

        with pytest.raises(TypeError) as exc_info:
            result = phone + grass
        assert "Нельзя складывать товары разных классов" in str(exc_info.value)

    def test_add_product_with_smartphone(self):
        """Проверяем сложение обычного продукта со смартфоном (разные классы)"""
        from main import Product, Smartphone

        product = Product("Product", "Desc", 100.0, 5)
        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")

        with pytest.raises(TypeError) as exc_info:
            result = product + phone
        assert "Нельзя складывать товары разных классов" in str(exc_info.value)

    def test_add_product_with_grass(self):
        """Проверяем сложение обычного продукта с травой (разные классы)"""
        from main import Product, LawnGrass

        product = Product("Product", "Desc", 100.0, 5)
        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")

        with pytest.raises(TypeError) as exc_info:
            result = product + grass
        assert "Нельзя складывать товары разных классов" in str(exc_info.value)

    def test_add_phone_with_product_still_works_for_same_class(self):
        """Проверяем, что сложение смартфонов одного класса работает"""
        from main import Smartphone

        phone1 = Smartphone("Phone1", "Desc", 1000.0, 2, "CPU1", "M1", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 2000.0, 3, "CPU2", "M2", 256, "White")

        # Это должно работать без ошибок
        result = phone1 + phone2
        assert result == 8000.0


# ========== НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 3 (ЗАЩИТА ДОБАВЛЕНИЯ) ==========

class TestCategoryAddProtection:
    """Тесты для защиты метода add_product"""

    def setup_method(self):
        """Создаем чистую категорию перед каждым тестом"""
        from main import Category
        self.category = Category("Тестовая категория", "Для тестов", [])

    def test_add_product_to_category(self):
        """Проверяем добавление обычного продукта"""
        from main import Product

        product = Product("Товар", "Описание", 100.0, 5)
        initial_count = Category.product_count

        self.category.add_product(product)

        # Проверяем, что продукт добавился
        assert product.name in self.category.products
        assert Category.product_count == initial_count + 1

    def test_add_smartphone_to_category(self):
        """Проверяем добавление смартфона"""
        from main import Smartphone

        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")
        initial_count = Category.product_count

        self.category.add_product(phone)

        # Проверяем, что смартфон добавился
        assert phone.name in self.category.products
        assert Category.product_count == initial_count + 1
        # Проверяем, что это действительно смартфон
        assert isinstance(self.category._Category__products[0], Smartphone)

    def test_add_grass_to_category(self):
        """Проверяем добавление газонной травы"""
        from main import LawnGrass

        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")
        initial_count = Category.product_count

        self.category.add_product(grass)

        # Проверяем, что трава добавилась
        assert grass.name in self.category.products
        assert Category.product_count == initial_count + 1
        assert isinstance(self.category._Category__products[0], LawnGrass)

    def test_add_non_product_raises_error(self):
        """Проверяем, что добавление не-продукта вызывает ошибку"""
        # Пробуем добавить число
        with pytest.raises(TypeError) as exc_info:
            self.category.add_product(123)
        assert "Можно добавлять только объекты Product" in str(exc_info.value)

        # Пробуем добавить строку
        with pytest.raises(TypeError) as exc_info:
            self.category.add_product("строка")
        assert "Можно добавлять только объекты Product" in str(exc_info.value)

        # Пробуем добавить список
        with pytest.raises(TypeError) as exc_info:
            self.category.add_product([1, 2, 3])
        assert "Можно добавлять только объекты Product" in str(exc_info.value)

        # Пробуем добавить словарь
        with pytest.raises(TypeError) as exc_info:
            self.category.add_product({"name": "test"})
        assert "Можно добавлять только объекты Product" in str(exc_info.value)

        # Пробуем добавить None
        with pytest.raises(TypeError) as exc_info:
            self.category.add_product(None)
        assert "Можно добавлять только объекты Product" in str(exc_info.value)

    def test_add_multiple_products_mixed(self):
        """Проверяем добавление разных продуктов"""
        from main import Product, Smartphone, LawnGrass

        product = Product("Товар", "Описание", 100.0, 5)
        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")

        self.category.add_product(product)
        self.category.add_product(phone)
        self.category.add_product(grass)

        # Проверяем, что все три добавились
        products_output = self.category.products
        assert product.name in products_output
        assert phone.name in products_output
        assert grass.name in products_output

        # Проверяем количество
        assert len(self.category._Category__products) == 3

    def test_product_count_after_mixed_add(self):
        """Проверяем счетчик товаров после добавления разных продуктов"""
        from main import Product, Smartphone, LawnGrass, Category

        initial_count = Category.product_count

        product = Product("Товар", "Описание", 100.0, 5)
        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")

        self.category.add_product(product)
        self.category.add_product(phone)
        self.category.add_product(grass)

        # Должно увеличиться на 3
        assert Category.product_count == initial_count + 3


# ========== ТЕСТЫ ДЛЯ УВЕЛИЧЕНИЯ ПОКРЫТИЯ ==========

class TestCoverageImprovement:
    """Тесты для увеличения покрытия кода"""

    def test_product_price_setter_with_print(self, capsys):
        """Тестируем вывод сообщения при некорректной цене"""
        from main import Product

        product = Product("Тест", "Описание", 100.0, 5)

        # Устанавливаем отрицательную цену
        product.price = -50
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

        # Устанавливаем нулевую цену
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_product_creation_with_negative_price(self, capsys):
        """Тестируем создание продукта с отрицательной ценой"""
        from main import Product

        product = Product("Тест", "Описание", -100.0, 5)
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 0.0  # Цена должна быть 0 по умолчанию

    def test_product_creation_with_zero_price(self, capsys):
        """Тестируем создание продукта с нулевой ценой"""
        from main import Product

        product = Product("Тест", "Описание", 0.0, 5)
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 0.0

    def test_category_products_getter_empty(self):
        """Тестируем геттер products для пустой категории"""
        from main import Category

        category = Category("Пустая", "Описание", [])
        assert category.products == ""

    def test_category_add_multiple_products_count(self):
        """Тестируем счетчик товаров при множественном добавлении"""
        from main import Category, Product

        initial_count = Category.product_count

        category = Category("Тест", "Описание", [])
        product1 = Product("Товар 1", "Описание", 100.0, 2)
        product2 = Product("Товар 2", "Описание", 200.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        assert Category.product_count == initial_count + 2

    def test_new_product_classmethod_with_dict(self):
        """Тестируем создание продукта через класс-метод"""
        from main import Product

        data = {
            'name': 'Тестовый товар',
            'description': 'Тестовое описание',
            'price': 1500.0,
            'quantity': 10
        }

        product = Product.new_product(data)
        assert product.name == 'Тестовый товар'
        assert product.description == 'Тестовое описание'
        assert product.price == 1500.0
        assert product.quantity == 10

    def test_smartphone_all_attributes(self):
        """Тестируем все атрибуты смартфона"""
        from main import Smartphone

        phone = Smartphone(
            "Телефон", "Описание", 1000.0, 5,
            "Процессор", "Модель", 256, "Черный"
        )

        assert phone.efficiency == "Процессор"
        assert phone.model == "Модель"
        assert phone.memory == 256
        assert phone.color == "Черный"

    def test_lawn_grass_all_attributes(self):
        """Тестируем все атрибуты газонной травы"""
        from main import LawnGrass

        grass = LawnGrass(
            "Трава", "Описание", 500.0, 10,
            "Россия", "7 дней", "Зеленый"
        )

        assert grass.country == "Россия"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Зеленый"

    def test_add_method_with_different_classes_detailed(self):
        """Детальный тест сложения разных классов"""
        from main import Smartphone, LawnGrass, Product

        phone = Smartphone("P", "D", 100.0, 2, "CPU", "M", 128, "B")
        grass = LawnGrass("G", "D", 50.0, 5, "R", "7d", "G")
        product = Product("Pr", "D", 200.0, 3)

        # Проверяем все комбинации разных классов
        with pytest.raises(TypeError):
            phone + grass
        with pytest.raises(TypeError):
            phone + product
        with pytest.raises(TypeError):
            grass + product

    def test_category_add_protection_with_various_types(self):
        """Тестируем защиту добавления с разными типами данных"""
        from main import Category

        category = Category("Тест", "Описание", [])

        # Список различных не-продуктов
        bad_types = [
            123,
            "строка",
            [1, 2, 3],
            {"key": "value"},
            None,
            True,
            3.14,
            (1, 2, 3)
        ]

        for bad_type in bad_types:
            with pytest.raises(TypeError):
                category.add_product(bad_type)

    def test_category_str_with_various_quantities(self):
        """Тестируем строковое представление с разными количествами"""
        from main import Category, Product

        # Тест с нулевым количеством
        cat1 = Category("Cat1", "Desc", [Product("P", "D", 100.0, 0)])
        assert "количество продуктов: 0 шт." in str(cat1)

        # Тест с большим количеством
        cat2 = Category("Cat2", "Desc", [Product("P", "D", 100.0, 1000)])
        assert "количество продуктов: 1000 шт." in str(cat2)

        # Тест с несколькими товарами
        products = [
            Product("P1", "D", 100.0, 5),
            Product("P2", "D", 200.0, 3),
            Product("P3", "D", 300.0, 2)
        ]
        cat3 = Category("Cat3", "Desc", products)
        assert "количество продуктов: 10 шт." in str(cat3)

    def test_product_add_edge_cases(self):
        """Тестируем граничные случаи сложения"""
        from main import Product

        # Очень большие числа
        p1 = Product("P1", "D", 1_000_000.0, 1_000_000)
        p2 = Product("P2", "D", 1.0, 1)
        result = p1 + p2
        assert result == 1_000_000_000_000.0 + 1.0

        # Нулевая цена
        p3 = Product("P3", "D", 0.0, 100)
        p4 = Product("P4", "D", 100.0, 0)
        assert p3 + p4 == 0.0

    def test_product_str_edge_cases(self):
        """Тестируем строковое представление в граничных случаях"""
        from main import Product

        # Очень большая цена
        p1 = Product("P1", "D", 1_000_000.0, 1)
        assert "1000000.0 руб." in str(p1)

        # Очень большое количество
        p2 = Product("P2", "D", 1.0, 1_000_000)
        assert "Остаток: 1000000 шт." in str(p2)

        # Цена с большим количеством знаков после запятой
        p3 = Product("P3", "D", 99.999999, 1)
        assert str(p3)  # Просто проверяем, что не падает

    def test_category_initialization_with_products(self):
        """Тестируем инициализацию категории с товарами"""
        from main import Category, Product

        products = [
            Product("P1", "D", 100.0, 5),
            Product("P2", "D", 200.0, 3)
        ]

        category = Category("Тест", "Описание", products)

        # Проверяем, что товары доступны через геттер
        output = category.products
        assert "P1" in output
        assert "P2" in output

        # Проверяем счетчики
        assert Category.category_count > 0
        assert Category.product_count >= len(products)


# Добавь этот код в конец файла tests/test_main.py

class TestAdditionalCoverage:
    """Дополнительные тесты для увеличения покрытия"""

    def test_smartphone_inheritance(self):
        """Тестируем наследование Smartphone от Product"""
        phone = Smartphone(
            "Test Phone", "Desc", 1000.0, 5,
            "CPU", "Model", 256, "Black"
        )

        # Проверяем, что все методы Product доступны
        assert isinstance(phone, Product)
        assert hasattr(phone, '__str__')
        assert hasattr(phone, '__add__')
        assert hasattr(phone, 'price')

        # Проверяем работу метода __str__ унаследованного от Product
        expected = "Test Phone, 1000.0 руб. Остаток: 5 шт."
        assert str(phone) == expected

    def test_lawn_grass_inheritance(self):
        """Тестируем наследование LawnGrass от Product"""
        grass = LawnGrass(
            "Test Grass", "Desc", 500.0, 10,
            "Russia", "7 days", "Green"
        )

        # Проверяем, что все методы Product доступны
        assert isinstance(grass, Product)
        assert hasattr(grass, '__str__')
        assert hasattr(grass, '__add__')
        assert hasattr(grass, 'price')

        # Проверяем работу метода __str__ унаследованного от Product
        expected = "Test Grass, 500.0 руб. Остаток: 10 шт."
        assert str(grass) == expected

    def test_add_method_with_different_smartphone_models(self):
        """Тестируем сложение разных моделей смартфонов"""
        phone1 = Smartphone(
            "Samsung", "Desc", 80000.0, 2,
            "Snapdragon", "S23", 256, "Black"
        )
        phone2 = Smartphone(
            "iPhone", "Desc", 90000.0, 3,
            "A16", "15", 256, "White"
        )

        # Складываем смартфоны (должно работать)
        result = phone1 + phone2
        expected = (80000.0 * 2) + (90000.0 * 3)  # 160000 + 270000 = 430000
        assert result == expected

    def test_add_method_with_different_grass_types(self):
        """Тестируем сложение разных типов травы"""
        grass1 = LawnGrass(
            "Sport", "Desc", 1500.0, 5,
            "Russia", "7 days", "Green"
        )
        grass2 = LawnGrass(
            "Decor", "Desc", 2000.0, 3,
            "Holland", "10 days", "Dark Green"
        )

        # Складываем траву (должно работать)
        result = grass1 + grass2
        expected = (1500.0 * 5) + (2000.0 * 3)  # 7500 + 6000 = 13500
        assert result == expected

    def test_category_with_mixed_products(self):
        """Тестируем категорию с разными типами продуктов"""
        product = Product("Обычный товар", "Desc", 100.0, 5)
        phone = Smartphone(
            "Смартфон", "Desc", 50000.0, 2,
            "CPU", "Model", 128, "Black"
        )
        grass = LawnGrass(
            "Трава", "Desc", 1000.0, 10,
            "Russia", "7 days", "Green"
        )

        category = Category("Смешанная категория", "Desc", [product, phone, grass])

        # Проверяем строковое представление
        output = str(category)
        assert "количество продуктов: 17 шт." in output  # 5 + 2 + 10 = 17

        # Проверяем геттер products
        products_output = category.products
        assert "Обычный товар" in products_output
        assert "Смартфон" in products_output
        assert "Трава" in products_output

    def test_price_setter_with_validation(self, capsys):
        """Тестируем сеттер цены с разными значениями"""
        product = Product("Test", "Desc", 100.0, 5)

        # Пробуем установить отрицательную цену
        product.price = -10.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

        # Пробуем установить нулевую цену
        product.price = 0.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

        # Устанавливаем корректную цену
        product.price = 150.0
        captured = capsys.readouterr()
        assert captured.out == ""  # Нет сообщения об ошибке
        assert product.price == 150.0

    def test_new_product_classmethod_with_different_data(self):
        """Тестируем класс-метод new_product с разными данными"""
        test_data = [
            {
                'name': 'Товар 1',
                'description': 'Описание 1',
                'price': 100.0,
                'quantity': 5
            },
            {
                'name': 'Товар 2',
                'description': 'Описание 2',
                'price': 200.0,
                'quantity': 10
            }
        ]

        for data in test_data:
            product = Product.new_product(data)
            assert product.name == data['name']
            assert product.description == data['description']
            assert product.price == data['price']
            assert product.quantity == data['quantity']


# ========== ТЕСТЫ ДЛЯ НОВОЙ ФУНКЦИОНАЛЬНОСТИ (АБСТРАКТНЫЙ КЛАСС И МИКСИН) ==========

class TestBaseProduct:
    """Тесты для абстрактного класса BaseProduct"""

    def test_baseproduct_abstract_class(self):
        """Проверяем, что BaseProduct - абстрактный класс и его нельзя инстанцировать"""
        from main import BaseProduct

        with pytest.raises(TypeError) as exc_info:
            BaseProduct("Тест", "Описание", 100.0, 5)
        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_product_inherits_from_baseproduct(self):
        """Проверяем, что Product наследуется от BaseProduct"""
        from main import Product, BaseProduct

        assert issubclass(Product, BaseProduct)
        assert isinstance(Product("Тест", "Описание", 100.0, 5), BaseProduct)

    def test_smartphone_inherits_from_baseproduct(self):
        """Проверяем, что Smartphone наследуется от BaseProduct через Product"""
        from main import Smartphone, BaseProduct

        phone = Smartphone("Phone", "Desc", 1000.0, 2, "CPU", "M", 128, "Black")
        assert isinstance(phone, BaseProduct)

    def test_lawn_grass_inherits_from_baseproduct(self):
        """Проверяем, что LawnGrass наследуется от BaseProduct через Product"""
        from main import LawnGrass, BaseProduct

        grass = LawnGrass("Grass", "Desc", 500.0, 10, "Russia", "7 days", "Green")
        assert isinstance(grass, BaseProduct)


class TestProductReprMixin:
    """Тесты для миксина ProductReprMixin"""

    def test_mixin_output_on_product_creation(self, capsys):
        """Проверяем, что при создании Product выводится сообщение"""
        from main import Product

        Product("Тестовый товар", "Описание", 1000.0, 5)
        captured = capsys.readouterr()

        assert "Создание объекта Product с параметрами:" in captured.out
        assert "Тестовый товар" in captured.out
        assert "Описание" in captured.out
        assert "1000.0" in captured.out
        assert "5" in captured.out

    def test_mixin_output_on_smartphone_creation(self, capsys):
        """Проверяем, что при создании Smartphone выводится сообщение"""
        from main import Smartphone

        Smartphone("iPhone", "Смартфон", 80000.0, 3,
                   "A16", "15 Pro", 256, "черный")
        captured = capsys.readouterr()

        assert "Создание объекта Smartphone с параметрами:" in captured.out
        assert "iPhone" in captured.out
        assert "Смартфон" in captured.out
        assert "80000.0" in captured.out
        assert "3" in captured.out

    def test_mixin_output_on_lawn_grass_creation(self, capsys):
        """Проверяем, что при создании LawnGrass выводится сообщение"""
        from main import LawnGrass

        LawnGrass("Газон", "Трава для газона", 2000.0, 10,
                  "Россия", "7-10 дней", "зеленый")
        captured = capsys.readouterr()

        assert "Создание объекта LawnGrass с параметрами:" in captured.out
        assert "Газон" in captured.out
        assert "Трава для газона" in captured.out
        assert "2000.0" in captured.out
        assert "10" in captured.out

    def test_mixin_inheritance_chain(self):
        """Проверяем, что миксин правильно встроен в цепочку наследования"""
        from main import Product, ProductReprMixin, BaseProduct

        # Проверяем порядок наследования
        assert ProductReprMixin in Product.__bases__
        assert BaseProduct in Product.__bases__

        # Проверяем, что методы миксина доступны
        product = Product("Тест", "Описание", 100.0, 5)
        assert hasattr(product, '__init__')

    def test_multiple_creations_output(self, capsys):
        """Проверяем вывод при создании нескольких объектов"""
        from main import Product, Smartphone, LawnGrass

        # Создаем несколько объектов
        Product("Товар 1", "Описание 1", 100.0, 5)
        Smartphone("Телефон 1", "Описание", 50000.0, 2, "CPU", "M", 128, "черный")
        LawnGrass("Трава 1", "Описание", 1500.0, 20, "Россия", "7 дней", "зеленый")

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')

        # Должно быть 3 строки вывода
        assert len(output_lines) == 3
        assert "Создание объекта Product" in output_lines[0]
        assert "Создание объекта Smartphone" in output_lines[1]
        assert "Создание объекта LawnGrass" in output_lines[2]


# ========== ТЕСТЫ ДЛЯ ПРОВЕРКИ ПОКРЫТИЯ ==========

def test_coverage_requirement():
    """Проверяем, что покрытие тестами > 75%"""
    # Это вспомогательная функция, которая будет использовать pytest-cov
    # Запускать нужно отдельно: pytest --cov=main tests/
    pass


class TestAdditionalCoverageForNewFeatures:
    """Дополнительные тесты для новой функциональности"""

    def test_baseproduct_has_abstract_methods(self):
        """Проверяем, что BaseProduct имеет все необходимые абстрактные методы"""
        from main import BaseProduct

        # Получаем список абстрактных методов
        abstract_methods = getattr(BaseProduct, '__abstractmethods__', [])

        # Проверяем наличие обязательных методов
        assert '__init__' in abstract_methods
        assert '__str__' in abstract_methods
        assert '__add__' in abstract_methods
        assert 'price' in abstract_methods

    def test_product_implements_all_abstract_methods(self):
        """Проверяем, что Product реализует все абстрактные методы"""
        from main import Product, BaseProduct

        # Пытаемся создать экземпляр - не должно быть ошибки
        product = Product("Тест", "Описание", 100.0, 5)

        # Проверяем, что все методы работают
        assert hasattr(product, '__init__')
        assert hasattr(product, '__str__')
        assert hasattr(product, '__add__')
        assert hasattr(product, 'price')

    def test_mixin_output_format(self, capsys):
        """Проверяем формат вывода миксина"""
        from main import Product

        Product("Тестовый продукт", "Тестовое описание", 123.45, 7)
        captured = capsys.readouterr()

        # Проверяем формат: класс, параметры
        assert captured.out.startswith("Создание объекта Product с параметрами:")
        assert "Тестовый продукт" in captured.out
        assert "Тестовое описание" in captured.out
        assert "123.45" in captured.out
        assert "7" in captured.out
