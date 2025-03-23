from bot import Bot
from database.database_manager import DatabaseManager
from assistants.shop_assistant import ShopAssistant
from generators.products_generator import ProductsGenerator

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

    user_input = ""

    while user_input != "0":
        print("--- Примеры интеграций больших языковых моделей в клиентоориентированные приложения ---")
        print("Выберите контекст для рассмотрения:\n1. Интернет-магазин электроники\n0. Выход")
        user_input = input("> ")

        if user_input == "1":
            # Инициализация помощника
            assistant = ShopAssistant(bot, db)

            # Генерация тестовых данных
            products_generator = ProductsGenerator(db)
            products_generator.generate(20)

            user_request = ""

            while user_request != "0":
                # Запрос пользователя
                user_request = input(
                    "Введите запрос для поиска подходящих товаров на естественном языке (0 для выхода из контекста): ")

                if user_request == "0":
                    break

                # Поиск товаров
                products = assistant.find_products(user_request)
                for product in products:
                    print(product)
        elif user_input == "0":
            print("Пока-пока!")
        else:
            print("Некорректный ввод!")
