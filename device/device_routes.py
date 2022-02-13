from logging import getLogger
from typing import Dict, List
from flask import Blueprint, current_app, jsonify
from cachetools import TTLCache, cached
import requests as r

from device.model.device import Device, DeviceResponse


DEVICE = Blueprint('device', __name__)

logger = getLogger()


@DEVICE.route('/device')
def get_all_devices_by_brand():
  devices = get_device_list_by_brands()
  return jsonify(devices)


@DEVICE.route('/device/<brand_key>')
def get_device_by_brand(brand_key: str):
  devices = get_device_list_by_brands()
  return jsonify(get_devices_by_key(brand_key, devices))


def get_devices_by_key(brand_key: str, brands: List['DeviceResponse']):
  for device in brands:
    if device.key == brand_key:
      return device.device_list
  return "Could not find this phone"


def parse_to_device_dataclass(device_list: List) -> List['Device']:
  return [Device(**device) for device in device_list]


def parse_response(data: List[Dict]) -> List[DeviceResponse]:
  data_list = []
  for res in data:
    devices = parse_to_device_dataclass(res.get('device_list', []))
    res['device_list'] = devices
    data_list.append(DeviceResponse(**res))
  return data_list


@cached(cache=TTLCache(maxsize=1000, ttl=3000))
def get_device_list_by_brands() -> Dict:
    logger.debug("Getting data from GSM ARENA API")
    GSM_ARENA_API_URL: str = current_app.config.get('GSM_ARENA_API_URL', '')
    req = r.get(GSM_ARENA_API_URL, {'route': 'device-list'})
    data: Dict = req.json()
    json_data = data.get('data', {})
    return parse_response(json_data)
