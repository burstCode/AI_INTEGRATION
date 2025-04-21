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
              "2. Обращение в скорую помощь\n"
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
            db_manager = MedicalDatabaseManager()
            assistant = MedicalAssistant(bot, db_manager)

            # Интерактивный диалог!
            while True:
                print("\n1. Создать новый тикет")
                print("2. Просмотреть последние тикеты")
                print("0. Выход")
                
                choice = input("Выберите действие: ")
                
                if choice == "1":
                    result = assistant.create_ticket()
                    print(result)
                elif choice == "2":
                    tickets = db_manager.get_tickets(5)
                    for ticket in tickets:
                        print(f"\nТикет #{ticket.id}")
                        print(f"Симптомы: {', '.join(ticket.symptoms)}")
                        print(f"Приоритет: {ticket.priority.display_name}")
                        print(f"Дата: {ticket.created_at.strftime('%Y-%m-%d %H:%M')}")
                elif choice == "0":
                    break
        elif user_input == "0":
            print("Пока-пока!")
        else:
            print("Некорректный ввод!")
