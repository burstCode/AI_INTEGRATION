from datetime import datetime

from models.product import Product
from models.medical_ticket import MedicalTicket

from typing import List, Dict

import sqlite3


class DatabaseManager:
    """
    Менеджер базы данных.
    Определяет методы для создания нужных таблиц и поиска.
    """

    db_path: str

    def __init__(self, db_path: str = "ai_integration.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Создает таблицы для данных всех примеров интеграции БЯМ.
        """

        self._create_table_products()
        self._create_table_medical_tickets()

    # ---------- Методы для работы с примером магазина электроники ----------

    def _create_table_products(self) -> None:
        """
        Создает таблицу с товарами.
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PRODUCTS (
                    PRODUCT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PRODUCT_NAME TEXT NOT NULL,
                    PRODUCT_CATEGORY TEXT NOT NULL,
                    PRODUCT_RAM TEXT,
                    PRODUCT_STORAGE TEXT,
                    PRODUCT_PROCESSOR TEXT,
                    PRODUCT_SCREEN_SIZE TEXT,
                    PRODUCT_GPU TEXT,
                    PRODUCT_RESOLUTION TEXT,
                    PRODUCT_REFRESH_RATE TEXT,
                    PRODUCT_TYPE TEXT,
                    PRODUCT_LAYOUT TEXT,
                    PRODUCT_BACKLIGHT TEXT,
                    PRODUCT_DPI TEXT,
                    PRODUCT_BUTTONS TEXT
                )
            """)
            conn.commit()

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в базу данных.

        :param product: Объект продукта, который надо добавить в базу данных.
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO 
                    PRODUCTS (
                        PRODUCT_NAME, PRODUCT_CATEGORY, PRODUCT_RAM,
                        PRODUCT_STORAGE, PRODUCT_PROCESSOR, PRODUCT_SCREEN_SIZE,
                        PRODUCT_GPU, PRODUCT_RESOLUTION, PRODUCT_REFRESH_RATE,
                        PRODUCT_TYPE, PRODUCT_LAYOUT, PRODUCT_BACKLIGHT,
                        PRODUCT_DPI, PRODUCT_BUTTONS
                        )
                    VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.product_name,
                product.product_category,
                product.product_specs.get("PRODUCT_RAM"),
                product.product_specs.get("PRODUCT_STORAGE"),
                product.product_specs.get("PRODUCT_PROCESSOR"),
                product.product_specs.get("PRODUCT_SCREEN_SIZE"),
                product.product_specs.get("PRODUCT_GPU"),
                product.product_specs.get("PRODUCT_RESOLUTION"),
                product.product_specs.get("PRODUCT_REFRESH_RATE"),
                product.product_specs.get("PRODUCT_TYPE"),
                product.product_specs.get("PRODUCT_LAYOUT"),
                product.product_specs.get("PRODUCT_BACKLIGHT"),
                product.product_specs.get("PRODUCT_DPI"),
                product.product_specs.get("PRODUCT_BUTTON"),
            ))
            conn.commit()

    def find_products(self, category: str, specs: Dict[str, str]) -> List[Product]:
        """
        Осуществляет поиск в базе данных по переданным категории и характеристикам.

        :param category: Категория товаров, в которой производится поиск.
        :param specs: Словарь характеристик товаров, по которым производится поиск.
        :return: Список найденных товаров
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT
                    PRODUCT_ID, PRODUCT_NAME, PRODUCT_CATEGORY,
                    PRODUCT_RAM, PRODUCT_STORAGE, PRODUCT_PROCESSOR,
                    PRODUCT_SCREEN_SIZE, PRODUCT_GPU, PRODUCT_RESOLUTION,
                    PRODUCT_REFRESH_RATE, PRODUCT_TYPE, PRODUCT_LAYOUT,
                    PRODUCT_BACKLIGHT, PRODUCT_DPI, PRODUCT_BUTTONS
                FROM
                    PRODUCTS
                WHERE
                    PRODUCT_CATEGORY = ?
                """

            params = [category]

            # Добавляем переданные в метод параметры для выборки
            for key, value in specs.items():
                if isinstance(value, list):
                    query += f" AND {key} IN ({', '.join(['?'] * len(value))})"
                    params.extend(value)
                else:
                    query += f" AND {key} = ?"
                    params.append(value)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Формируем список объектов Product
            products = []
            for row in rows:
                product_specs = {
                    "PRODUCT_RAM": row[3],
                    "PRODUCT_STORAGE": row[4],
                    "PRODUCT_PROCESSOR": row[5],
                    "PRODUCT_SCREEN_SIZE": row[6],
                    "PRODUCT_GPU": row[7],
                    "PRODUCT_RESOLUTION": row[8],
                    "PRODUCT_REFRESH_RATE": row[9],
                    "PRODUCT_TYPE": row[10],
                    "PRODUCT_LAYOUT": row[11],
                    "PRODUCT_BACKLIGHT": row[12],
                    "PRODUCT_DPI": row[13],
                    "PRODUCT_BUTTONS": row[14],
                }

                # Убираем None значения из словаря
                product_specs = {k: v for k, v in product_specs.items() if v is not None}

                new_product = Product(row[0], row[1], row[2], product_specs)

                products.append(new_product)

            return products

    # ---------- Методы для работы с примером обращений в скорую ----------

    def _create_table_medical_tickets(self) -> None:
        """
        Создает таблицу с обращениями в скорую.
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                   CREATE TABLE IF NOT EXISTS MEDICAL_TICKETS (
                       MEDICAL_TICKET_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       MEDICAL_TICKET_SYMPTOMS TEXT NOT NULL,
                       MEDICAL_TICKET_CREATED_AT TEXT NOT NULL,
                       MEDICAL_TICKET_PRIORITY TEXT NOT NULL,
                       MEDICAL_TICKET_PATIENT_INFO TEXT,
                       MEDICAL_TICKET_STATUS TEXT NOT NULL
                   )
               """)
            conn.commit()

    def add_medical_ticket(self, medical_ticket: MedicalTicket) -> None:
        """
        Добавляет обращение в базу данных.

        :param medical_ticket: Объект медицинского обращения, который надо добавить в базу данных.
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO 
                    MEDICAL_TICKETS (
                        MEDICAL_TICKET_SYMPTOMS, MEDICAL_TICKET_CREATED_AT,
                        MEDICAL_TICKET_PRIORITY, MEDICAL_TICKET_PATIENT_INFO,
                        MEDICAL_TICKET_STATUS
                    )
                    VALUES (?, ?, ?, ?, ?)
            """
            , (
                    ",".join(medical_ticket.medical_ticket_symptoms),
                    medical_ticket.medical_ticket_created_at.isoformat(),
                    medical_ticket.medical_ticket_priority,
                    medical_ticket.medical_ticket_patient_info,
                    medical_ticket.medical_ticket_status
            ))
            conn.commit()

    def get_tickets(self) -> List[MedicalTicket]:
        """
        Получает все обращения в скорую в порядке, начиная с последних добавленных
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    MEDICAL_TICKET_ID, MEDICAL_TICKET_SYMPTOMS, MEDICAL_TICKET_CREATED_AT,
                    MEDICAL_TICKET_PRIORITY, MEDICAL_TICKET_PATIENT_INFO, MEDICAL_TICKET_STATUS
                FROM
                    MEDICAL_TICKETS
                ORDER BY
                    MEDICAL_TICKET_CREATED_AT DESC
            """)

            # Формируем список обращений в скорую
            medical_tickets = []
            for row in cursor.fetchall():
                new_medical_ticket = MedicalTicket(
                    row[0],
                    row[1].split(","),
                    datetime.fromisoformat(row[2]),
                    row[3],
                    row[4],
                    row[5]
                )

                medical_tickets.append(new_medical_ticket)

            return medical_tickets

    def get_tickets_sorted(self) -> List[MedicalTicket]:
        """
        Возвращает обращения, отсортированные по приоритету и времени
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    MEDICAL_TICKET_ID, MEDICAL_TICKET_SYMPTOMS, MEDICAL_TICKET_CREATED_AT,
                    MEDICAL_TICKET_PRIORITY, MEDICAL_TICKET_PATIENT_INFO, MEDICAL_TICKET_STATUS
                FROM 
                    MEDICAL_TICKETS
                ORDER BY
                    CASE MEDICAL_TICKET_STATUS
                            WHEN 'Новый' THEN 1
                            WHEN 'В работе' THEN 2
                            WHEN 'Завершен' THEN 3
                            ELSE 4
                    END, 
                    CASE MEDICAL_TICKET_PRIORITY
                        WHEN 'КРИТИЧЕСКИЙ' THEN 1
                        WHEN 'Высокий' THEN 2
                        WHEN 'Средний' THEN 3
                        WHEN 'Низкий' THEN 4
                        ELSE 5
                    END,
                    MEDICAL_TICKET_CREATED_AT DESC
            """)
            return self._rows_to_tickets(cursor.fetchall())

    def update_ticket_status(self, ticket_id: int, new_status: str):
        """Обновляет статус обращения"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE MEDICAL_TICKETS
                SET MEDICAL_TICKET_STATUS = ?
                WHERE MEDICAL_TICKET_ID = ?
            """, (new_status, ticket_id))
            conn.commit()

    def _rows_to_tickets(self, rows) -> List[MedicalTicket]:
        tickets = []
        for row in rows:
            tickets.append(MedicalTicket(
                row[0],
                row[1].split(','),
                datetime.fromisoformat(row[2]),
                row[3],
                row[4],
                row[5]
            ))
        return tickets
