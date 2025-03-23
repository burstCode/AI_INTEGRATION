from models.product import Product

from typing import Dict, List
import sqlite3


class DatabaseManager:
    """
    Менеджер базы данных. Создает таблицы и позволяет работать с ними
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
        """

                :param category: Категория товара
                :param specs: Словарь характеристик товара
                :return: Список найденных товаров
                """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT name, category, ram, storage, processor, screen_size, gpu, resolution, refresh_rate, type, layout, backlight, dpi, buttons FROM products WHERE category = ?"
            params = [category]

            for key, value in specs.items():
                if isinstance(value, list):
                    # Если значение — список, используем оператор IN
                    query += f" AND {key} IN ({', '.join(['?'] * len(value))})"
                    params.extend(value)
                else:
                    # Если значение — строка, используем оператор =
                    query += f" AND {key} = ?"
                    params.append(value)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                Product(
                    name=row[0],
                    category=row[1],
                    specs={key: row[i + 2] for i, key in enumerate(specs.keys())}
                )
                for row in rows
            ]
