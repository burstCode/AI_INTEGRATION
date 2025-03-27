from faker import Faker

from database.database_manager import DatabaseManager
from models.product import Product

# Списки характеристик
CATEGORIES = ["ноутбуки", "настольные компьютеры", "мониторы", "клавиатуры", "мыши"]
RAM_OPTIONS = ["8 ГБ", "16 ГБ", "32 ГБ"]
STORAGE_OPTIONS = ["256 ГБ SSD", "512 ГБ SSD", "1 ТБ SSD", "1 ТБ HDD", "2 ТБ HDD"]
PROCESSOR_OPTIONS = ["Intel i5", "Intel i7", "AMD Ryzen 5", "AMD Ryzen 7"]
SCREEN_SIZE_OPTIONS = ["13 дюймов", "15 дюймов", "17 дюймов", "24 дюйма", "27 дюймов", "32 дюйма"]
GPU_OPTIONS = ["NVIDIA GTX 1660", "NVIDIA RTX 3060", "AMD Radeon RX 6700"]
RESOLUTION_OPTIONS = ["1080p", "1440p", "4K"]
REFRESH_RATE_OPTIONS = ["60 Гц", "144 Гц", "240 Гц"]
KEYBOARD_TYPE_OPTIONS = ["мембранная", "механическая"]
KEYBOARD_LAYOUT_OPTIONS = ["ANSI", "ISO"]
KEYBOARD_BACKLIGHT_OPTIONS = ["да", "нет"]
MOUSE_TYPE_OPTIONS = ["проводная", "беспроводная"]
MOUSE_DPI_OPTIONS = ["800", "1600", "3200"]
MOUSE_BUTTONS_OPTIONS = ["2", "5", "7"]


class ProductsGenerator:
    """
    Генератор продуктов
    """

    db: DatabaseManager
    faker: Faker

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.fake = Faker()

    def generate(self, products_amount: int) -> None:
        """
        Генерирует указанное количество товаров.
        :paPRODUCT_RAM products_amount: Количество товаров, требуемое для генерации.
        """

        products = []

        for _ in range(products_amount):  # Генерируем 20 товаров
            category = self.fake.random_element(CATEGORIES)
            products.append(self._generate_product(category))

        self._insert_products(products)
        print(f"Сгенерировано и добавлено {len(products)} товаров.")

    def _insert_products(self, products: list):
        """
        Вставляет товары в базу данных.
        :paPRODUCT_RAM products: Список товаров, которые нужно вставить в базу данных.
        """

        for product in products:
            self.db.add_product(product)

    def _generate_product(self, category: str) -> Product:
        """
        Генерирует случайный товар с характеристиками в зависимости от категории.
        """
        specs = {}

        if category == "ноутбуки":
            specs.update({
                "PRODUCT_RAM": self.fake.random_element(RAM_OPTIONS),
                "PRODUCT_STORAGE": self.fake.random_element(STORAGE_OPTIONS),
                "PRODUCT_PROCESSOR": self.fake.random_element(PROCESSOR_OPTIONS),
                "PRODUCT_SCREEN_SIZE": self.fake.random_element(SCREEN_SIZE_OPTIONS),
            })
        elif category == "настольные компьютеры":
            specs.update({
                "PRODUCT_RAM": self.fake.random_element(RAM_OPTIONS),
                "PRODUCT_STORAGE": self.fake.random_element(STORAGE_OPTIONS),
                "PRODUCT_PROCESSOR": self.fake.random_element(PROCESSOR_OPTIONS),
                "PRODUCT_GPU": self.fake.random_element(GPU_OPTIONS),
            })
        elif category == "мониторы":
            specs.update({
                "PRODUCT_SCREEN_SIZE": self.fake.random_element(SCREEN_SIZE_OPTIONS),
                "PRODUCT_RESOLUTION": self.fake.random_element(RESOLUTION_OPTIONS),
                "PRODUCT_REFRESH_RATE": self.fake.random_element(REFRESH_RATE_OPTIONS),
            })
        elif category == "клавиатуры":
            specs.update({
                "PRODUCT_TYPE": self.fake.random_element(KEYBOARD_TYPE_OPTIONS),
                "PRODUCT_LAYOUT": self.fake.random_element(KEYBOARD_LAYOUT_OPTIONS),
                "PRODUCT_BACKLIGHT": self.fake.random_element(KEYBOARD_BACKLIGHT_OPTIONS),
            })
        elif category == "мыши":
            specs.update({
                "PRODUCT_TYPE": self.fake.random_element(MOUSE_TYPE_OPTIONS),
                "PRODUCT_DPI": self.fake.random_element(MOUSE_DPI_OPTIONS),
                "BUTTONS": self.fake.random_element(MOUSE_BUTTONS_OPTIONS),
            })

        product = Product(
            0,
            self.fake.word().capitalize() + " " + self.fake.word().capitalize(),
            category,
            specs
        )

        print(f"Сгенерирован товар: {product}")

        return product
