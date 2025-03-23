import re
from datetime import datetime, timedelta
from typing import Optional, List

from bot import Bot
from database.reservation_database_manager import ReservationDatabaseManager
from models.reservation import Table, Reservation

import json

class ReservationAssistant:
    bot: Bot
    db: ReservationDatabaseManager

    def __init__(self, bot: Bot, db: ReservationDatabaseManager):
        self.bot = bot
        self.db = db

    def parse_user_request(self, user_request: str) -> Optional[dict]:
        """
        Преобразует запрос пользователя в структурированные данные.

        :param user_request: Запрос пользователя на естественном языке
        :return: Словарь с параметрами бронирования или None, если не удалось распознать запрос
        """
        prompt = f"""
        Пользователь хочет забронировать столик в ресторане. Извлеки из его запроса параметры бронирования и верни их в формате JSON.
        Параметры:
        - guests: Количество гостей (целое число, по умолчанию 2)
        - date: Дата в формате ГГГГ-ММ-ДД
        - time: Время в формате ЧЧ:ММ
        - duration: Длительность бронирования в минутах (целое число, по умолчанию 120)

        Запрос пользователя: {user_request}

        Ответ должен быть без какого-либо форматирования, например:
        {{
            "guests": 2,
            "date": "2023-10-25",
            "time": "19:00",
            "duration": 120
        }}
        """
        response = self.bot.send_request(prompt)
        print(f"Ответ нейросети: {response}")
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return None

    def find_available_table(self, guests: int, start_time: datetime, duration: timedelta) -> Optional[Table]:
        """Находит доступный столик для указанного времени."""

        available_tables = self.db.get_available_tables(guests, start_time, duration)
        return available_tables[0] if available_tables else None

    def suggest_alternative_time(self, guests: int, start_time: datetime, duration: timedelta) -> Optional[datetime]:
        """Предлагает ближайшее доступное время для бронирования."""

        current_time = start_time
        while current_time.hour < 22:  # Ресторан работает до 22:00
            if self.find_available_table(guests, current_time, duration):
                return current_time
            current_time += timedelta(minutes=30)  # Проверяем каждые 30 минут
        return None

    def make_reservation(self, user_request: str) -> str:
        """
        Обрабатывает запрос пользователя и создает бронирование.

        :param user_request: Запрос пользователя на естественном языке
        :return: Сообщение о результате бронирования
        """

        data = self.parse_user_request(user_request)
        if not data:
            return "Не удалось распознать запрос. Пожалуйста, уточните детали."

        guests = data["guests"]
        start_time = datetime.fromisoformat(f"{data['date']}T{data['time']}")
        duration = timedelta(minutes=data.get("duration", 120))

        # Пытаемся найти доступный столик
        table = self.find_available_table(guests, start_time, duration)
        if table:
            reservation = Reservation(
                table_id=table.id,
                start_time=start_time,
                duration=duration,
                guests=guests,
            )
            self.db.add_reservation(reservation)
            return f"Столик #{table.id} на {guests} человек успешно забронирован на {start_time.strftime('%Y-%m-%d %H:%M')}."

        # Если столик недоступен, предлагаем альтернативное время
        alternative_time = self.suggest_alternative_time(guests, start_time, duration)
        if alternative_time:
            return f"Свободных столиков на указанное время нет. Ближайшее доступное время: {alternative_time.strftime('%Y-%m-%d %H:%M')}."
        return "К сожалению, свободных столиков на сегодня больше нет."