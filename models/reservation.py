from dataclasses import dataclass
from datetime import datetime, timedelta


# Обалдеть! Вон че в питончике есть занятное
@dataclass
class Reservation:
    table_id: int      # Идентификатор столика
    start_time: datetime  # Время начала бронирования
    duration: timedelta   # Длительность бронирования
    guests: int           # Количество гостей

@dataclass
class Table:
    id: int       # Уникальный идентификатор столика
    capacity: int # Вместимость (количество человек)