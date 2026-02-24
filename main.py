# main.py

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
        # Проверяем, что other - тоже Product
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")

        # Проверяем, что классы одинаковые (используем type())
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        # Если все проверки пройдены - складываем
        return (self.price * self.quantity) + (other.price * other.quantity)

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


class Smartphone(Product):
    """Класс для смартфонов, наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        # Вызываем конструктор родительского класса
        super().__init__(name, description, price, quantity)

        # Добавляем новые атрибуты
        self.efficiency = efficiency  # производительность
        self.model = model  # модель
        self.memory = memory  # объем встроенной памяти
        self.color = color  # цвет


class LawnGrass(Product):
    """Класс для газонной травы, наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        # Вызываем конструктор родительского класса
        super().__init__(name, description, price, quantity)

        # Добавляем новые атрибуты
        self.country = country  # страна-производитель
        self.germination_period = germination_period  # срок прорастания
        self.color = color  # цвет


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

    @property
    def products(self):
        """Геттер для получения форматированного списка товаров"""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"  # ИСПОЛЬЗУЕМ __str__ продукта
        return result


def main():
    """Основная функция программы"""
    # Здесь можно оставить минимальный код или вообще ничего
    pass


if __name__ == "__main__":
    main()
