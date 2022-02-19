from dataclasses import dataclass, field
from typing import List
from device.model.device import Device


@dataclass
class User():
  id: int
  username: str
  password: str
  posts: List = field(default_factory=lambda: [])
  device: Device = field(default_factory=lambda: Device())
