class Product:
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str,
                 products: list):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def main():
    """Основная функция программы"""
    product1 = Product(
        name="Samsung Galaxy S23",
        description="256GB, Серый цвет",
        price=87000.0,
        quantity=5
    )
    product2 = Product(
        name="iPhone 15",
        description="512GB, Черный цвет",
        price=95000.0,
        quantity=3
    )

    category = Category(
        name="Смартфоны",
        description="Мобильные устройства",
        products=[product1, product2]
    )

    print(f"Категория: {category.name}")
    print(f"Количество товаров в категории: {len(category.products)}")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\nИнформация о товарах:")
    for product in category.products:
        print(f"- {product.name}: {product.price} руб., "
              f"остаток: {product.quantity} шт.")


if __name__ == "__main__":
    main()
