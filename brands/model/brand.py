from dataclasses import dataclass


@dataclass
class Brand:
    "Brand id - like: 1, 2"
    brand_id: int
    "Brand name - Nokia"
    brand_name: str
    "Accessor for brand - nokia it's a key"
    key: str
