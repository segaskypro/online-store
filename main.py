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

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)  # Добавляем в приватный список
        Category.product_count += 1  # Увеличиваем счетчик товаров

    @property
    def products(self):
        """Геттер для получения форматированного списка товаров"""
        result = ""  # Начинаем с пустой строки
        for product in self.__products:  # Проходим по приватному списку
            # Форматируем каждый товар по шаблону
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
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

    # Проверяем, что оба продукта созданы правильно
    print("\nПроверка созданных товаров:")
    print(f"product1: {product1.name}, {product1.price} руб.")
    print(f"product2: {product2.name}, {product2.price} руб.")
    print(f"Тип product2: {type(product2)}")


if __name__ == "__main__":
    main()
