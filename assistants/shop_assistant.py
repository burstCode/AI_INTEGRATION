from bot import Bot
from models.product import Product
from database.database_manager import DatabaseManager

from typing import List, Dict, Optional
import json


class ShopAssistant:
    """
    Ассистент магазина электроники: позволяет пользователю подобрать товар
    """

    bot: Bot
    db: DatabaseManager

    def __init__(self, bot: Bot, db: DatabaseManager):
        """
        :param bot: Экземпляр класса Bot для взаимодействия с нейросетью.
        :param db: Экземпляр менеджера базы данных для взаимодействия с базой данных.
        """

        self.bot = bot
        self.db = db

    def parse_user_request(self, user_request: str) -> Optional[Dict[str, str | List[str]]]:
        prompt = f"""
        Пользователь хочет купить товар. Извлеки из его запроса параметры товара и верни их в формате JSON.
        Будь внимателен к тому, что подходящих товаров может быть несколько.
        Доступные категории: ноутбуки, настольные компьютеры, мониторы, клавиатуры, мыши.
        При определении подходящей категории указывай ее в том же виде, что и в списке выше.
        Характеристики:
        - Ноутбуки: PRODUCT_RAM (8 ГБ, 16 ГБ, 32 ГБ), PRODUCT_STORAGE (256 ГБ SSD, 512 ГБ SSD, 1 ТБ SSD), PRODUCT_PROCESSOR (Intel i5, Intel i7, AMD Ryzen 5, AMD Ryzen 7), PRODUCT_SCREEN_SIZE (13 дюймов, 15 дюймов, 17 дюймов)
        - Настольные компьютеры: PRODUCT_RAM (8 ГБ, 16 ГБ, 32 ГБ), PRODUCT_STORAGE (512 ГБ SSD, 1 ТБ HDD, 2 ТБ HDD), PRODUCT_PROCESSOR (Intel i5, Intel i7, AMD Ryzen 5, AMD Ryzen 7), PRODUCT_GPU (NVIDIA GTX 1660, NVIDIA RTX 3060, AMD Radeon RX 6700)
        - Мониторы: PRODUCT_SCREEN_SIZE (24 дюйма, 27 дюймов, 32 дюйма), PRODUCT_RESOLUTION (1080p, 1440p, 4K), PRODUCT_REFRESH_RATE (60 Гц, 144 Гц, 240 Гц)
        - Клавиатуры: PRODUCT_TYPE (мембранная, механическая), PRODUCT_LAYOUT (ANSI, ISO), PRODUCT_BACKLIGHT (да, нет)
        - Мыши: PRODUCT_TYPE (проводная, беспроводная), PRODUCT_DPI (800, 1600, 3200), PRODUCT_BUTTONS (2, 5, 7)
        
        Ответ нужно присылать без лишних знаков форматирования, например:
        {{
            "PRODUCT_CATEGORY": "ноутбук",
            "PRODUCT_SPECS": {{
                "PRODUCT_RAM": "16 ГБ",
                "PRODUCT_STORAGE": "512 ГБ SSD",
                ...
            }}
        }}
        
        Если из ответа пользователя ясно, что он хочет ознакомиться с товарами разных характеристик, то запиши характеристики в виде списка, например:
        {{
            "PRODUCT_CATEGORY": "мышь",
            "PRODUCT_SPECS": {{
                "PRODUCT_BUTTONS": ["2", "5"],
                ...
            }}
        }}

        Запрос пользователя: {user_request} 
        """
        response = self.bot.send_request(prompt)
        print(f"Ответ нейросети: {response}")

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return None

    def find_products(self, user_request: str) -> List[Product]:
        product_params = self.parse_user_request(user_request)
        if not product_params:
            return []
        return self.db.find_products(product_params["PRODUCT_CATEGORY"], product_params.get("PRODUCT_SPECS", {}))
