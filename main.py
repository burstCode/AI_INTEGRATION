from assistants.medical_assistent import MedicalAssistant
from assistants.reservation_assistant import ReservationAssistant
from bot import Bot
from database.medical_database_manager import MedicalDatabaseManager
from database.shop_database_manager  import ShopDatabaseManager
from assistants.shop_assistant import ShopAssistant
from database.reservation_database_manager import ReservationDatabaseManager
from generators.products_generator import ProductsGenerator

import config


if __name__ == "__main__":
    # Вытягиваем из конфига переменные для настройки бота
    endpoint = config.ENDPOINT
    github_token = config.GITHUB_TOKEN
    model_name = config.MODEL_NAME

    # Инициализируем бота
    bot = Bot(endpoint, github_token, model_name)

    user_input = ""

    while user_input != "0":
        print("--- Примеры интеграций больших языковых моделей в клиентоориентированные приложения ---")
        print("Выберите контекст для рассмотрения:\n"
              "1. Интернет-магазин электроники\n"
              "2. Бронирование столика в ресторане\n"
              "3. Обращение в скорую помощь\n"
              "0. Выход")
        user_input = input("> ")

        if user_input == "1":
            # Инициализация базы данных
            db = ShopDatabaseManager()

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
        elif user_input == "2":
            # Инициализация базы данных
            db = ReservationDatabaseManager()

            # Инициализация помощника
            assistant = ReservationAssistant(bot, db)

            user_request = ""

            while user_request != "0":
                # Запрос пользователя
                user_request = input(
                    "Введите запрос на естественном языке для бронирования столика (0 для выхода из контекста): ")

                if user_request == "0":
                    break

                result = assistant.make_reservation(user_request)
                print(result)
        elif user_input == "3":
            # Инициализация БД
            db_manager = MedicalDatabaseManager()

            # Инициализация ассистента
            assistant = MedicalAssistant(bot, db_manager)

            user_input = ""

            while user_input != "0":
                user_request = input("На естественном языке введите запрос к службе скорой, например, опишите "
                                     "симптомы (0 для выхода из контекста): ")

                if user_request == "0":
                    break

                result = assistant.create_ticket(user_request)
                print(result)

                # Вывод всех тикетов
                print("\nПоследние тикеты:")
                for ticket in db_manager.get_tickets(5):
                    print(f"#{ticket.id} [{ticket.priority.value}]: {', '.join(ticket.symptoms)}")
        elif user_input == "0":
            print("Пока-пока!")
        else:
            print("Некорректный ввод!")
