from dataclasses import dataclass
from math import inf
from random import randint


@dataclass
class Post:
 title: str
 description: str
 id: int = randint(0, inf)
