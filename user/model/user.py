from dataclasses import dataclass, field
from typing import List, Optional
from device.model.device import Device


@dataclass
class User:
  uid: str
  email: str
  password: str = ""
  photo_url: str = ""
  display_name: str = ""
  posts: List = field(default_factory=lambda: [])
  device: Optional[Device] = field(default_factory=lambda: None)
