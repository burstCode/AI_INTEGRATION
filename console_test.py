from bot import Bot

from database.database_manager import DatabaseManager

from assistants.medical_assistent import MedicalAssistant
from assistants.shop_assistant import ShopAssistant

from generators.products_generator import ProductsGenerator

import config


# Вытягиваем из конфига переменные для настройки бота
endpoint = config.ENDPOINT
github_token = config.GITHUB_TOKEN
model_name = config.MODEL_NAME

# Инициализируем бота
bot = Bot(endpoint, github_token, model_name)
db = DatabaseManager()

user_input = ""

while user_input != "0":
    print("--- Примеры интеграций больших языковых моделей в клиентоориентированные приложения ---")
    print("Выберите контекст для рассмотрения:\n"
          "1. Интернет-магазин электроники\n"
          "2. Обращение в скорую помощь\n"
          "0. Выход")
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

            if not products:
                print("Ничего не найдено по вашему запросу!")

            for product in products:
                print(product)
    elif user_input == "2":
        # Инициализация ассистента
        assistant = MedicalAssistant(bot, db)

        user_input = ""

        while user_input != "0":
            user_request = input("На естественном языке введите запрос к службе скорой, например, опишите "
                                 "симптомы (0 для выхода из контекста): ")

            if user_request == "0":
                break

            medical_ticket = assistant.parse_user_request(user_request)

            if medical_ticket is None:
                print("Запрос не содержит подходящей информации для обращения в скорую")
                break

            db.add_medical_ticket(medical_ticket)
            # result = assistant.create_ticket(user_request)
            # print(result)

            # Вывод всех тикетов
            print("\nПоследние тикеты:")
            for medical_ticket in db.get_tickets():
                print(
                    f"#{medical_ticket.medical_ticket_id} [{medical_ticket.medical_ticket_priority}]: {', '.join(medical_ticket.medical_ticket_symptoms)}")
    elif user_input == "0":
        print("Пока-пока!")
    else:
        print("Некорректный ввод!")


"""
Описать текстом в виде статьи                                                                           ( )
Прикинуть многоступенчатый диалог (в общем случае уточнения со стороны нейросети при неуверенности      ( )
Промпты усложить (сделать бронебойными)                                                                 (+)
Можно накидать сайтик для примера с магазином/скорой службой, hell yeah                                 ( )
"""
