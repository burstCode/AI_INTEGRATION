from typing import Dict


class Product:
    name: str
    category: str
    specs: Dict[str, str]

    def __init__(self, name: str, category: str, specs: Dict[str, str]):
        """

        :param name: Название товара
        :param category: Категория товара
        :param specs: Характеристики товара
        """

        self.name = name
        self.category = category
        self.specs = specs

    def __repr__(self) -> str:
        return f"Product(name={self.name}, category={self.category}, specs={self.specs})"
