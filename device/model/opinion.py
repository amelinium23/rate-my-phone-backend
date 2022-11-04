from dataclasses import field, dataclass
from typing import Optional, Dict, Any
from uuid import uuid4


@dataclass
class Opinion:
    device_id: str
    title: str
    description: str
    uid: str
    user: Optional[Dict[str, Any]] = None
    id: str = field(default_factory=lambda: str(uuid4()))
