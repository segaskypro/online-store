# main.py
from abc import ABC, abstractmethod


class ProductReprMixin:
    """Миксин для вывода информации о создании объекта"""

    def __init__(self, *args, **kwargs):
        print(f"Создание объекта {self.__class__.__name__} с параметрами: {args}, {kwargs}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Конструктор, который должен быть у каждого продукта"""
        pass

    @abstractmethod
    def __str__(self):
        """Строковое представление, которое должно быть у каждого продукта"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Сложение продуктов, которое должно быть у каждого продукта"""
        pass

    @property
    @abstractmethod
    def price(self):
        """Геттер цены, который должен быть у каждого продукта"""
        pass


class Product(ProductReprMixin, BaseProduct):
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        # Проверяем количество товара
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.quantity = quantity
        self.__price = 0.0
        self.price = price

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_dict):
        return cls(
            name=product_dict['name'],
            description=product_dict['description'],
            price=product_dict['price'],
            quantity=product_dict['quantity']
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Smartphone(Product):
    """Класс для смартфонов, наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)

        # Добавляем новые атрибуты
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы, наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)

        # Добавляем новые атрибуты
        self.country = country
        self.germination_period = germination_period
        self.color = color

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
        # Проверяем, что product является экземпляром Product или его наследников
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")

        self.__products.append(product)  # Добавляем в приватный список
        Category.product_count += 1  # Увеличиваем счетчик товаров

    def average_price(self):
        """Подсчитывает средний ценник всех товаров в категории"""
        try:
            total_sum = 0
            for product in self.__products:
                total_sum += product.price
            return total_sum / len(self.__products)
        except ZeroDivisionError:
            return 0


    @property
    def products(self):
        """Геттер для получения форматированного списка товаров"""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"  # ИСПОЛЬЗУЕМ __str__ продукта
        return result


def main():
    """Основная функция программы"""
    print("=== Демонстрация исключения при quantity=0 ===\n")

    try:
        print("Пытаемся создать товар с количеством 0...")
        product = Product("Тест", "Описание", 100.0, 0)
        print("Товар создался (не должно быть!)")
    except ValueError as e:
        print(f"Поймана ошибка: {e}")
        print("✅ Исключение работает правильно!")

# def main():
#     """Основная функция программы"""
#     print("=== Начинаем тестирование миксина ===\n")
#
#     # Создаем обычный продукт
#     product1 = Product("Телефон", "Смартфон Apple", 90000, 10)
#
#     # Создаем смартфон
#     phone = Smartphone("iPhone 14", "Смартфон Apple", 80000, 5,
#                        "высокая", "14 Pro", 256, "черный")
#
#     # Создаем газонную траву
#     grass = LawnGrass("Газон City", "Трава для газона", 2000, 20,
#                       "Россия", "10 дней", "зеленый")
#
#     print("\n=== Все продукты успешно созданы ===")


if __name__ == "__main__":
    main()
