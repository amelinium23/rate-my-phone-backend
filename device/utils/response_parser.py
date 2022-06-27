from typing import Dict, List, Optional

from device.model.device import Device, DeviceResponse


def _get_devices_by_key(brand_key: str, brands: List['DeviceResponse']) -> Optional['Device']:
  for device in brands:
    if device.key == brand_key:
      return device.device_list
  return None


def _parse_to_device_dataclass(device_list: List) -> List['Device']:
  return [Device(**device) for device in device_list]


def _parse_response(data: List[Dict]) -> List[DeviceResponse]:
  data_list = []
  for res in data:
    devices = _parse_to_device_dataclass(res.get('device_list', []))
    res['device_list'] = devices
    data_list.append(DeviceResponse(**res))
  return data_list
