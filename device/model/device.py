from dataclasses import dataclass
from typing import List


@dataclass
class Device:
  key: str
  device_name: str
  device_id: int
  device_type: str
  device_image: str


@dataclass
class DeviceResponse:
  brand_id: int
  brand_name: str
  key: str
  device_list: List['Device']