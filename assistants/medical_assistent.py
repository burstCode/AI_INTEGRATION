import json
from datetime import datetime
from typing import Optional

from bot import Bot
from database.database_manager import DatabaseManager
from models.medical_ticket import MedicalTicket


class MedicalAssistant:
    """
    Ассистент службы скорой помощи. Позволяет пользователю создать обращение в скорую помощь
    """

    def __init__(self, bot: Bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db = db_manager

    def parse_user_request(self, user_input: str) -> Optional[MedicalTicket]:
        """
        Анализирует симптомы и создает обращение в скорую
        """
        prompt = f"""
        Ты медицинский ассистент. Проанализируй описание симптомов и верни JSON:
        {{
            "symptoms": ["список", "симптомов"],
            "priority": "Низкий|Средний|Высокий|КРИТИЧЕСКИЙ",
            "patient_info": "str"|null
        }}

        Правила определения приоритета:
        - Низкий: Легкие симптомы (насморк, небольшой кашель)
        - Средний: Умеренные (температура до 38, боль в горле)
        - Высокий: Серьезные (температура выше 38, сильная боль)
        - КРИТИЧЕСКИЙ: Опасные для жизни (потеря сознания, затрудненное дыхание)

        В ответе верни json без какого-либо форматирования.
        
        Обращение пользователя: "{user_input}"
        """

        response = self.bot.send_request(prompt)
        print(f"Ответ нейросети: {response}")

        try:
            data = json.loads(response)

            new_medical_ticket = MedicalTicket(
                0,
                data["symptoms"],
                datetime.now(),
                data["priority"],
                data.get("patient_info"),
                "Новый"
            )

            return new_medical_ticket
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка парсинга ответа: {e}")
            return None

    # def create_ticket(self, user_input: str) -> str:
    #     """
    #     Создает обращение на основе описания симптомов
    #     """
    #
    #     medical_ticket = self.parse_user_request(user_input)
    #     if not medical_ticket:
    #         return "Не удалось обработать описание симптомов. Пожалуйста, уточните детали."
    #
    #     ticket_id = self.db.add_ticket(medical_ticket)
    #     return (f"Медицинский тикет #{ticket_id} создан.\n"
    #             f"Симптомы: {', '.join(medical_ticket.symptoms)}\n"
    #             f"Приоритет: {medical_ticket.priority.value}\n"
    #             f"Статус: {medical_ticket.status}")