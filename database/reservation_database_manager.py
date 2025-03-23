import sqlite3
from datetime import datetime, timedelta
from typing import List

from models.reservation import Table, Reservation


class ReservationDatabaseManager:
    """
    Менеджер базы данных броней. Создает соответсвующую таблицу и позволяет работать с данными в ней
    """

    def __init__(self, db_path: str = "ai_integration.db"):
        self.db_path = db_path
        self._create_tables()
        self._seed_tables()  # Заполняем базу тестовыми столиками

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    capacity INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    guests INTEGER NOT NULL,
                    FOREIGN KEY (table_id) REFERENCES tables (id)
                )
            """)
            conn.commit()

    def _seed_tables(self):
        """Заполняет базу тестовыми столиками"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tables")
            if cursor.fetchone()[0] == 0:
                cursor.executemany("""
                    INSERT INTO tables (capacity) VALUES (?)
                """, [
                    (2,),  # Столик на 2 человека
                    (4,),  # Столик на 4 человека
                    (6,),  # Столик на 6 человек
                ])
                conn.commit()

    def get_available_tables(self, guests: int, start_time: datetime, duration: timedelta) -> List[Table]:
        """Возвращает список доступных столиков для указанного количества гостей и времени"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, capacity FROM tables
                WHERE capacity >= ?
                AND id NOT IN (
                    SELECT table_id FROM reservations
                    WHERE (
                        -- Начало нового бронирования внутри существующего
                        ? >= start_time AND ? < datetime(start_time, '+' || duration || ' seconds')
                        OR
                        -- Окончание нового бронирования внутри существующего
                        datetime(?, '+' || ? || ' seconds') > start_time AND datetime(?, '+' || ? || ' seconds') <= datetime(start_time, '+' || duration || ' seconds')
                        OR
                        -- Новое бронирование полностью перекрывает существующее
                        ? <= start_time AND datetime(?, '+' || ? || ' seconds') >= datetime(start_time, '+' || duration || ' seconds')
                    )
                )
            """, (
                guests,
                start_time.isoformat(), start_time.isoformat(),
                start_time.isoformat(), duration.total_seconds(),
                start_time.isoformat(), duration.total_seconds(),
                start_time.isoformat(), start_time.isoformat(), duration.total_seconds(),
            ))
            return [Table(id=row[0], capacity=row[1]) for row in cursor.fetchall()]

    def add_reservation(self, reservation: Reservation):
        """Добавляет бронирование в базу данных"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservations (table_id, start_time, duration, guests)
                VALUES (?, ?, ?, ?)
            """, (
                reservation.table_id,
                reservation.start_time.isoformat(),
                reservation.duration.total_seconds(),
                reservation.guests,
            ))
            conn.commit()