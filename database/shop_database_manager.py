from models.product import Product

from typing import Dict, List
import sqlite3


class ShopDatabaseManager:
    """
    Менеджер базы данных магазина. Создает соответсвующую таблицу и позволяет работать с данными в ней
    """

    def __init__(self, db_path: str = "ai_integration.db"):
        """

        :param db_path: имя базы данных, по умолчанию - ai_integration.db
        """

        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Создает таблицы для примеров, если их не существует
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    ram TEXT,
                    storage TEXT,
                    processor TEXT,
                    screen_size TEXT,
                    gpu TEXT,
                    resolution TEXT,
                    refresh_rate TEXT,
                    type TEXT,
                    layout TEXT,
                    backlight TEXT,
                    dpi TEXT,
                    buttons TEXT
                )
            """)
            conn.commit()

    def add_product(self, product: Product):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, category, ram, storage, processor, screen_size, gpu, resolution, refresh_rate, type, layout, backlight, dpi, buttons)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.name,
                product.category,
                product.specs.get("ram"),
                product.specs.get("storage"),
                product.specs.get("processor"),
                product.specs.get("screen_size"),
                product.specs.get("gpu"),
                product.specs.get("resolution"),
                product.specs.get("refresh_rate"),
                product.specs.get("type"),
                product.specs.get("layout"),
                product.specs.get("backlight"),
                product.specs.get("dpi"),
                product.specs.get("buttons"),
            ))
            conn.commit()

    def find_products(self, category: str, specs: Dict[str, str | List[str]]) -> List[Product]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT name, category, ram, storage, processor, screen_size, gpu, resolution, refresh_rate, type, layout, backlight, dpi, buttons FROM products WHERE category = ?"
            params = [category]

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
                # Создаем словарь specs на основе данных из базы
                product_specs = {
                    "ram": row[2],
                    "storage": row[3],
                    "processor": row[4],
                    "screen_size": row[5],
                    "gpu": row[6],
                    "resolution": row[7],
                    "refresh_rate": row[8],
                    "type": row[9],
                    "layout": row[10],
                    "backlight": row[11],
                    "dpi": row[12],
                    "buttons": row[13],
                }
                # Убираем None значения из словаря
                product_specs = {k: v for k, v in product_specs.items() if v is not None}

                # Создаем объект Product
                products.append(Product(
                    name=row[0],
                    category=row[1],
                    specs=product_specs
                ))

            return products
