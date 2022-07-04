from device.utils.response_parser import get_devices_by_key, parse_response
from . import DEVICE
from typing import Dict, List
from flask import Response, jsonify
from cachetools import TTLCache, cached
from device.model.device import DeviceResponse
from utils.gsm_arena_utils import get_from_gsm_arena, post_to_gsm_arena


@DEVICE.route('/')
def get_all_devices_by_brand() -> Response:
  devices = get_device_list_by_brands()
  return jsonify(devices)


@DEVICE.route('/<brand_key>')
def get_device_by_brand(brand_key: str) -> Response:
  devices = get_device_list_by_brands()
  return jsonify(get_devices_by_key(brand_key, devices))


@DEVICE.route('/recommended')
def get_recommended_devices() -> Response:
  recommended = get_recommended_devices()
  return jsonify(recommended)


@DEVICE.route('/details/<device_key>', methods=['GET'])
def get_details_of_device(device_key: str) -> Response:
  device_detail = get_device_detail_from_api(device_key)
  return jsonify(device_detail)


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_device_list_by_brands() -> List[DeviceResponse]:
  data: Dict = get_from_gsm_arena({'route': 'device-list'})
  json_data = data.get('data', {})
  return parse_response(json_data)


def get_device_detail_from_api(device_key: str) -> Dict:
  data: Dict = post_to_gsm_arena({'route': 'device-detail', 'key': device_key})
  return data.get('data', {})


def get_recommended_devices() -> Dict:
  data: Dict = get_from_gsm_arena({}, "?route=recommended")
  return data.get('data', {})
