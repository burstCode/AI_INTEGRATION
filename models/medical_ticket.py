from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def display_name(self):
        names = {
            "LOW": "Низкий",
            "MEDIUM": "Средний",
            "HIGH": "Высокий",
            "CRITICAL": "Критический"
        }
        return names[self.value]

@dataclass
class MedicalTicket:
    id: int | None  # None для новых тикетов
    symptoms: list[str]
    created_at: datetime
    priority: Priority
    patient_info: str | None = None  # Дополнительная информация о пациенте
    status: str = "Новый"  # Статус обработки
