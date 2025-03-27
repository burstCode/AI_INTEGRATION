from dataclasses import dataclass
from typing import Dict


@dataclass(init=True, repr=True)
class Product:
    product_id: int
    product_name: str
    product_category: str
    product_specs: Dict[str, str]
