from dataclasses import dataclass, field
from random import randint
from typing import List, Optional
from forum.model.post_type import PostType


@dataclass
class Comment:
    id: int = randint(0, 10000000000000000)
    comment: Optional[str] = None
    votes: int = 0


@dataclass
class Post:
    title: str
    description: str
    uid: str
    type: str = PostType.DISCUSSION.value
    id: int = randint(0, 10000000000000000)
    votes: int = 0
    images: List[str] = field(default_factory=lambda: [])
    comments: List[Comment] = field(default_factory=lambda: [])
