from dataclasses import dataclass, field
from typing import List
from forum.model.post_type import PostType


@dataclass
class Comment:
    uid: str
    id: str = ""
    votes: int = 0
    comment: str = ""


@dataclass
class Post:
    title: str
    description: str
    uid: str
    id: str = ""
    type: str = PostType.DISCUSSION.value
    device_key: str = ""
    votes: int = 0
    images: List[str] = field(default_factory=lambda: [])
    comments: List[Comment] = field(default_factory=lambda: [])
