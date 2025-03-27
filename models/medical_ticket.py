from dataclasses import dataclass
from datetime import datetime


@dataclass(init=True, repr=True)
class MedicalTicket:
    medical_ticket_id: int
    medical_ticket_symptoms: list[str]
    medical_ticket_created_at: datetime
    medical_ticket_priority: str   # НИЗКИЙ, СРЕДНИЙ, ВЫСОКИЙ, КРИТИЧЕСКИЙ
    medical_ticket_patient_info: str | None = None  # Дополнительная информация о пациенте
    medical_ticket_status: str = "Новый"
