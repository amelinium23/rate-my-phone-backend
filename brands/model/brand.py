from dataclasses import dataclass


@dataclass
class Brand:
  brand_id: int
  "Brand id - like: 1, 2"
  brand_name: str
  "Brand name - Nokia"
  key: str
  "Accessor for brand - nokia it's a key"
