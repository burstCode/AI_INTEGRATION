import sqlite3
from datetime import datetime
from typing import List

from models.medical_ticket import MedicalTicket, Priority


class MedicalDatabaseManager:
    def __init__(self, db_path: str = "ai_integration.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symptoms TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    patient_info TEXT,
                    status TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_ticket(self, ticket: MedicalTicket) -> int:
        if not ticket.symptoms:
            raise ValueError("Тикет должен содержать хотя бы один симптом")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tickets (symptoms, created_at, priority, patient_info, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                ",".join(ticket.symptoms),
                ticket.created_at.isoformat(),
                ticket.priority.value,  # Используем value из enum
                ticket.patient_info,
                ticket.status
            ))
            conn.commit()
            return cursor.lastrowid

    def get_tickets(self, limit: int = 100) -> List[MedicalTicket]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, symptoms, created_at, priority, patient_info, status
                FROM tickets
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            tickets = []
            for row in cursor.fetchall():
                try:
                    priority = Priority(row[3].upper())  # Приводим к верхнему регистру
                except ValueError:
                    priority = Priority.MEDIUM  # Значение по умолчанию

                tickets.append(MedicalTicket(
                    id=row[0],
                    symptoms=row[1].split(","),
                    created_at=datetime.fromisoformat(row[2]),
                    priority=priority,
                    patient_info=row[4],
                    status=row[5]
                ))
            return tickets
