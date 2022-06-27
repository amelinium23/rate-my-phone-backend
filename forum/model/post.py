from dataclasses import dataclass
from random import randint


@dataclass
class Post:
 title: str
 description: str
 id: int = randint(0, 10000000000000000)
