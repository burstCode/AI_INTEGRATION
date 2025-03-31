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
        Ты медицинский ассистент, выступаешь как оператор скорой помощи. Проанализируй обращение пользователя на
        симптомы, на которые пользователь жалуется, а также на наличие какой-либо дополнительной информации о нем
        и верни JSON:
        {{
            "symptoms": ["список", "симптомов"],
            "priority": "Низкий|Средний|Высокий|КРИТИЧЕСКИЙ",
            "patient_info": "str"|null,
            "occurancy": int
        }}
        Если дополнительная информация о пользователе (например, его имя, возраст, адрес проживания) отсутствуют,
        то оставь в "patient_info" null.

        Правила определения приоритета:
        - Низкий: Легкие симптомы (насморк, небольшой кашель)
        - Средний: Умеренные (температура до 38, боль в горле)
        - Высокий: Серьезные (температура выше 38, сильная боль)
        - КРИТИЧЕСКИЙ: Опасные для жизни (потеря сознания, затрудненное дыхание)
        
        В переменную occurancy запиши значение от 0 до 100, обозначающее то, насколько хорошо ты понял запрос 
        пользователя. Значение меньше 50 означает, что в обращении пользователя отсутствуют смысл или какие-либо
        жалобы. 

        В ответе верни json без какого-либо форматирования.
        
        Обращение пользователя: "{user_input}"
        """

        response = self.bot.send_request(prompt)
        print(f"Ответ нейросети: {response}")

        try:
            data = json.loads(response)

            occurancy = int(data["occurancy"])

            if occurancy < 50:
                return None

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

    def create_ticket(self, user_input: str) -> int:
        """
        Создает обращение на основе описания симптомов
        """

        medical_ticket = self.parse_user_request(user_input)
        if not medical_ticket:
            return 1
            # return "Не удалось обработать описание симптомов. Пожалуйста, уточните детали."

        self.db.add_medical_ticket(medical_ticket)

        # return "Зарегистрировано новое обращение"
        return 0
