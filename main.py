# Разработка main

class Product:
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.quantity = quantity
        # Устанавливаем начальное значение
        self.__price = 0.0
        # Пробуем установить реальную цену через сеттер
        self.price = price  # Это вызовет @price.setter!

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сложение продуктов: возвращает сумму стоимости всех товаров на складе"""
        if isinstance(other, Product):  # Проверяем, что other - тоже Product
            return (self.price * self.quantity) + (other.price * other.quantity)
        else:
            raise TypeError("Можно складывать только объекты Product")

    @classmethod
    def new_product(cls, product_dict):
        """Класс-метод для создания нового продукта из словаря"""
        return cls(
            name=product_dict['name'],
            description=product_dict['description'],
            price=product_dict['price'],
            quantity=product_dict['quantity']
        )

    @property
    def price(self):
        """Геттер для получения цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для установки цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str,
                 products: list):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)  # Добавляем в приватный список
        Category.product_count += 1  # Увеличиваем счетчик товаров

    @property
    def products(self):
        """Геттер для получения форматированного списка товаров"""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"  # ИСПОЛЬЗУЕМ __str__ продукта
        return result


def main():
    """Основная функция программы"""
    print("=== Тестирование геттера и сеттера ===")

    # Создаем продукт
    product1 = Product(
        name="Samsung Galaxy S23",
        description="256GB, Серый цвет",
        price=87000.0,
        quantity=5
    )

    print(f"Исходная цена: {product1.price} руб.")  # Используем геттер

    # Пробуем установить правильную цену
    product1.price = 85000.0  # Используем сеттер
    print(f"Новая цена после уменьшения: {product1.price} руб.")

    # Пробуем установить нулевую цену (должно вывести сообщение)
    print("\nПопытка установить нулевую цену:")
    product1.price = 0  # Должно вывести сообщение об ошибке

    # Пробуем установить отрицательную цену
    print("\nПопытка установить отрицательную цену:")
    product1.price = -1000  # Должно вывести сообщение об ошибке

    # Проверяем, что цена не изменилась
    print(f"\nЦена после попыток установить некорректные значения: {product1.price} руб. (должна остаться 85000.0)")

    print("\n" + "=" * 50 + "\n")

    # Новый способ создания через класс-метод
    product_data = {
        'name': 'iPhone 15',
        'description': '512GB, Черный цвет',
        'price': 95000.0,
        'quantity': 3
    }
    product2 = Product.new_product(product_data)  # Используем класс-метод!

    category = Category(
        name="Смартфоны",
        description="Мобильные устройства",
        products=[product1, product2]
    )

    # Тестируем метод add_product
    product3 = Product(
        name="Xiaomi Redmi Note 13",
        description="128GB, Синий цвет",
        price=25000.0,
        quantity=10
    )
    category.add_product(product3)

    print(f"Категория: {category.name}")
    print(f"Количество товаров в категории: {len(category._Category__products)}")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\nИнформация о товарах:")
    print(category.products)

    print("\n=== Проверка магических методов __str__ ===")

    # Проверяем __str__ для продукта
    print("Товар через __str__:")
    print(product1)
    print(product2)
    print(product3)

    # Проверяем __str__ для категории
    print("\nКатегория через __str__:")
    print(category)

    print("\n=== Проверка магического метода __add__ ===")

    # Складываем два продукта
    product_a = Product("Товар A", "Описание", 100, 10)
    product_b = Product("Товар B", "Описание", 200, 2)

    result = product_a + product_b
    print(f"{product_a.name}: {product_a.price} × {product_a.quantity} = {product_a.price * product_a.quantity}")
    print(f"{product_b.name}: {product_b.price} × {product_b.quantity} = {product_b.price * product_b.quantity}")
    print(f"Сумма: {result} (должно быть 1400)")

    # Проверяем с нашими реальными продуктами
    print("\nСкладываем реальные товары из магазина:")
    sum1 = product1 + product2
    print(f"{product1.name}: {product1.price} × {product1.quantity} = {product1.price * product1.quantity}")
    print(f"{product2.name}: {product2.price} × {product2.quantity} = {product2.price * product2.quantity}")
    print(f"Сумма: {sum1}")

    # Проверяем, что будет ошибка при сложении с числом
    print("\nПопытка сложить продукт с числом (должна быть ошибка):")
    try:
        wrong = product1 + 100
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Проверяем, что старый products геттер работает так же
    print("\nСтарый геттер products (для сравнения):")
    print(category.products)

    # Проверяем, что оба продукта созданы правильно
    print("\nПроверка созданных товаров:")
    print(f"product1: {product1.name}, {product1.price} руб.")
    print(f"product2: {product2.name}, {product2.price} руб.")
    print(f"Тип product2: {type(product2)}")


if __name__ == "__main__":
    main()
