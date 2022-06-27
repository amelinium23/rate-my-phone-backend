from . import DEVICE
from typing import Dict, List, Optional
from flask import Response, jsonify
from cachetools import TTLCache, cached
from device.model.device import Device, DeviceResponse
from utils.gsm_arena_utils import get_from_gsm_arena, post_to_gsm_arena


@DEVICE.route('/')
def get_all_devices_by_brand() -> Response:
  """Endpoint for getting all devices

  Returns:
      Response: list of devices sorted by brands
  """
  devices = get_device_list_by_brands()
  return jsonify(devices)


@DEVICE.route('/<brand_key>')
def get_device_by_brand(brand_key: str) -> Response:
  """Endpoint for getting all devices by brand

  Args:
      brand_key (str): brand key i.e.: nokia

  Returns:
      Dict: all data from gsm arena api with devices sorted by brand
  """
  devices = get_device_list_by_brands()
  return jsonify(_get_devices_by_key(brand_key, devices))


@DEVICE.route('/recommended')
def get_recommended_devices() -> Response:
  """Getting recommended devices by GSMARENA

  Returns:
      Response: Response with json of recommended listings
  """
  recommended = get_recommended_devices()
  return jsonify(recommended)


@DEVICE.route('/details/<device_key>', methods=['GET'])
def get_details_of_device(device_key: str) -> Response:
  """Getting device detail from with api key

  Args:
      device_key (str): device key

  Returns:
      Dict: dict with all of the data from GSM ARENA API
  """
  device_detail = get_device_detail_from_api(device_key)
  return jsonify(device_detail)


def _get_devices_by_key(brand_key: str, brands: List['DeviceResponse']) -> Optional['Device']:
  """Get device by key

  Returns:
      Optional['Device']: device object
  """
  for device in brands:
    if device.key == brand_key:
      return device.device_list
  return None


def _parse_to_device_dataclass(device_list: List) -> List['Device']:
  """Function for parsing json object to device dataclass

  Returns:
      List['Device']: list of parsed devices
  """
  return [Device(**device) for device in device_list]


def _parse_response(data: List[Dict]) -> List[DeviceResponse]:
  data_list = []
  for res in data:
    devices = _parse_to_device_dataclass(res.get('device_list', []))
    res['device_list'] = devices
    data_list.append(DeviceResponse(**res))
  return data_list


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_device_list_by_brands() -> List[DeviceResponse]:
  """Function for getting parsed response from GSMARENA API

  Returns:
      List[DeviceResponse]: Data with responses
  """
  data: Dict = get_from_gsm_arena({'route': 'device-list'})
  json_data = data.get('data', {})
  return _parse_response(json_data)


def get_device_detail_from_api(device_key: str) -> Dict:
  """Function for getting devices details

  Args:
      device_key (str): key for searching in api i.e.: samsung_galaxy_s21_5g-10626

  Returns:
      Dict: device detail
  """
  data: Dict = post_to_gsm_arena({'route': 'device-detail', 'key': device_key})
  return data.get('data', {})


def get_recommended_devices() -> Dict:
  """Getting recommended listings from gsm arena

  Returns:
      Dict: dict with all data
  """
  data: Dict = get_from_gsm_arena({}, "?route=recommended")
  return data.get('data', {})
