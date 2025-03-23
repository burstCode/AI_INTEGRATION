from bot import Bot
from models.product import Product
from database.shop_database_manager import ShopDatabaseManager

from typing import List, Dict, Optional
import json


class ShopAssistant:
    bot: Bot
    db: ShopDatabaseManager

    def __init__(self, bot: Bot, db: ShopDatabaseManager):
        """
        :param bot: Экземпляр класса Bot для взаимодействия с нейросетью
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
        - Ноутбуки: ram (8 ГБ, 16 ГБ, 32 ГБ), storage (256 ГБ SSD, 512 ГБ SSD, 1 ТБ SSD), processor (Intel i5, Intel i7, AMD Ryzen 5, AMD Ryzen 7), screen_size (13 дюймов, 15 дюймов, 17 дюймов)
        - Настольные компьютеры: ram (8 ГБ, 16 ГБ, 32 ГБ), storage (512 ГБ SSD, 1 ТБ HDD, 2 ТБ HDD), processor (Intel i5, Intel i7, AMD Ryzen 5, AMD Ryzen 7), gpu (NVIDIA GTX 1660, NVIDIA RTX 3060, AMD Radeon RX 6700)
        - Мониторы: screen_size (24 дюйма, 27 дюймов, 32 дюйма), resolution (1080p, 1440p, 4K), refresh_rate (60 Гц, 144 Гц, 240 Гц)
        - Клавиатуры: type (мембранная, механическая), layout (ANSI, ISO), backlight (да, нет)
        - Мыши: type (проводная, беспроводная), dpi (800, 1600, 3200), buttons (2, 5, 7)
        
        Ответ нужно присылать без лишних знаков форматирования, например:
        {{
            "category": "ноутбук",
            "specs": {{
                "ram": "16 ГБ",
                "storage": "512 ГБ SSD",
                ...
            }}
        }}
        
        Если из ответа пользователя ясно, что он хочет ознакомиться с товарами разных характеристик, то запиши характеристики в виде списка, например:
        {{
            "category": "мышь",
            "specs": {{
                "buttons": ["2", "5"],
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
        return self.db.find_products(product_params["category"], product_params.get("specs", {}))
