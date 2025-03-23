from bot import Bot
from database.database_manager import DatabaseManager
from assistants.shopassistant import ShopAssistant
from models.product import Product

import config


if __name__ == "__main__":
    # Вытягиваем из конфига переменные для настройки бота
    endpoint = config.ENDPOINT
    github_token = config.GITHUB_TOKEN
    model_name = config.MODEL_NAME

    # Инициализируем бота
    bot = Bot(endpoint, github_token, model_name)

    # Инициализация базы данных
    db = DatabaseManager()

    # Добавление тестовых данных
    # db.add_product(Product(name="Ноутбук A", category="ноутбуки",
    #                        specs={"ram": "16 ГБ", "storage": "512 ГБ SSD", "processor": "Intel i7"}))
    # db.add_product(Product(name="Ноутбук B", category="ноутбуки",
    #                        specs={"ram": "32 ГБ", "storage": "1 ТБ SSD", "processor": "AMD Ryzen 7"}))

    # Инициализация помощника
    assistant = ShopAssistant(bot, db)

    # Запрос пользователя
    user_request = "Мне нужен ноутбук с 16 или 32 ГБ оперативной памяти"

    # Поиск товаров
    products = assistant.find_products(user_request)
    for product in products:
        print(product)
