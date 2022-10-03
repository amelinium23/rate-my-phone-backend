from dataclasses import dataclass, field
from typing import List, Optional
from forum.model.post_type import PostType
from uuid import uuid1


@dataclass
class Comment:
    id: str = str(uuid1())
    comment: Optional[str] = None
    votes: int = 0


@dataclass
class Post:
    title: str
    description: str
    uid: str
    id: str = str(uuid1())
    type: str = PostType.DISCUSSION.value
    device_key: str = ""
    votes: int = 0
    images: List[str] = field(default_factory=lambda: [])
    comments: List[Comment] = field(default_factory=lambda: [])
