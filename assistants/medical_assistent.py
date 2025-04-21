import json
from datetime import datetime
from typing import Optional, Dict, Any

from bot import Bot
from database.medical_database_manager import MedicalDatabaseManager
from models.medical_ticket import Priority, MedicalTicket


class MedicalAssistant:
    def __init__(self, bot: Bot, db_manager: MedicalDatabaseManager):
        self.bot = bot
        self.db = db_manager
        self.current_state = {}  # Для хранения промежуточных данных

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Парсит ответ нейросети и возвращает словарь с данными и уверенностью"""
        try:
            response = response.strip()
            if not response.startswith("{"):
                start = response.find("{")
                end = response.rfind("}") + 1
                response = response[start:end]
            
            data = json.loads(response)
            
            # Добавляем уверенность по умолчанию, если не указана
            if "confidence" not in data:
                data["confidence"] = 1.0
                
            return data
        except Exception as e:
            print(f"Ошибка парсинга ответа: {str(e)}")
            return {"confidence": 0, "message": "Не удалось разобрать ответ"}

    def _ask_clarification(self, missing_info: str, context: str) -> str:
        """Запрашивает уточнение у пользователя"""
        prompt = f"""
        Пациент предоставил информацию: "{context}"
        Но следующий параметр не ясен: {missing_info}
        
        Попроси пользователя уточнить эту информацию вежливо и профессионально.
        Верни только текст вопроса без дополнительных комментариев.
        """
        return self.bot.send_request(prompt).strip()

    def analyze_symptoms(self, initial_input: str) -> Optional[MedicalTicket]:
        """Многоступенчатый анализ симптомов с уточнениями"""
        context = initial_input
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            # Формируем запрос с учетом текущего контекста
            prompt = f"""
            Ты медицинский ассистент. Проанализируй описание симптомов и верни JSON:
            {{
                "symptoms": ["список", "симптомов"],
                "priority": "LOW|MEDIUM|HIGH|CRITICAL",
                "confidence": 0.0-1.0  # Уверенность в анализе
            }}

            Правила:
            1. Если что-то неясно, укажи confidence < 0.7 для этого параметра
            2. Для симптомов: верни массив, даже если один симптом
            3. Для priority: используй только указанные значения

            Контекст: "{context}"
            """
            
            response = self.bot.send_request(prompt)
            data = self._parse_response(response)
            
            # Проверяем уверенность в данных
            if data.get("confidence", 0) >= 0.7:
                try:
                    priority = Priority[data["priority"].upper()]
                    symptoms = [s.strip() for s in data["symptoms"] if s.strip()]
                    
                    if not symptoms:
                        raise ValueError("Нет симптомов")
                        
                    return MedicalTicket(
                        id=None,
                        symptoms=symptoms,
                        created_at=datetime.now(),
                        priority=priority,
                        patient_info=context
                    )
                except Exception as e:
                    print(f"Ошибка создания тикета: {str(e)}")
                    data["confidence"] = 0.5  # Принудительно понижаем уверенность
            
            # Если уверенность низкая, уточняем
            clarification_needed = []
            if data.get("confidence", 0) < 0.7:
                clarification_needed.append("общее состояние")
            elif len(data.get("symptoms", [])) < 1:
                clarification_needed.append("симптомы")
            elif "priority" not in data:
                clarification_needed.append("степень срочности")
            
            if clarification_needed:
                question = self._ask_clarification(
                    ", ".join(clarification_needed),
                    context
                )
                print(question)
                user_response = input("Ваш ответ: ")
                context += f". Уточнение: {user_response}"
                attempts += 1
            else:
                break
        
        return None

    def create_ticket(self) -> str:
        """Интерактивное создание тикета с уточнениями"""
        print("\nОпишите ваши симптомы (например: 'болит голова и температура'):")
        user_input = input("> ")
        
        ticket = self.analyze_symptoms(user_input)
        while ticket is None:
            print("\nПожалуйста, уточните ваши симптомы:")
            additional_input = input("> ")
            user_input += ". " + additional_input
            ticket = self.analyze_symptoms(user_input)
        
        ticket_id = self.db.add_ticket(ticket)
        return (f"\nМедицинский тикет #{ticket_id} создан.\n"
                f"Симптомы: {', '.join(ticket.symptoms)}\n"
                f"Приоритет: {ticket.priority.display_name}\n"
                f"Статус: {ticket.status}")
