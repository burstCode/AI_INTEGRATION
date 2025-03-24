import json
from datetime import datetime
from typing import Optional

from bot import Bot
from database.medical_database_manager import MedicalDatabaseManager
from models.medical_ticket import Priority, MedicalTicket


class MedicalAssistant:
    def __init__(self, bot: Bot, db_manager: MedicalDatabaseManager):
        self.bot = bot
        self.db = db_manager

    def analyze_symptoms(self, user_input: str) -> Optional[MedicalTicket]:
        """Анализирует симптомы и создает медицинский тикет"""
        prompt = f"""
        Ты медицинский ассистент. Проанализируй описание симптомов и верни JSON:
        {{
            "symptoms": ["список", "симптомов"],
            "priority": "LOW|MEDIUM|HIGH|CRITICAL"
        }}

        Правила определения приоритета:
        - LOW: Легкие симптомы (насморк, небольшой кашель)
        - MEDIUM: Умеренные (температура до 38, боль в горле)
        - HIGH: Серьезные (температура выше 38, сильная боль)
        - CRITICAL: Опасные для жизни (потеря сознания, затрудненное дыхание)

        В ответе верни json без какого-либо форматирования.
        
        Обращение пользователя: "{user_input}"
        """

        try:
            response = self.bot.send_request(prompt).strip()
            if not response.startswith("{"):
                # Ищем JSON в ответе, если он вложен в текст
                start = response.find("{")
                end = response.rfind("}") + 1
                response = response[start:end]

            data = json.loads(response)

            # Нормализация приоритета
            priority_str = data["priority"].upper().strip()
            try:
                priority = Priority(priority_str)
            except ValueError:
                priority = Priority.MEDIUM

            # Нормализация симптомов
            symptoms = [s.strip() for s in data["symptoms"] if s.strip()]

            return MedicalTicket(
                id=None,
                symptoms=symptoms,
                created_at=datetime.now(),
                priority=priority,
                patient_info=user_input
            )
        except Exception as e:
            print(f"Ошибка анализа симптомов: {str(e)}")
            print(f"Ответ нейросети: {response}")
            return None

    def create_ticket(self, user_input: str) -> str:
        """Создает тикет на основе описания симптомов"""

        ticket = self.analyze_symptoms(user_input)
        if not ticket:
            return "Не удалось обработать описание симптомов. Пожалуйста, уточните детали."

        ticket_id = self.db.add_ticket(ticket)
        return (f"Медицинский тикет #{ticket_id} создан.\n"
                f"Симптомы: {', '.join(ticket.symptoms)}\n"
                f"Приоритет: {ticket.priority.value}\n"
                f"Статус: {ticket.status}")