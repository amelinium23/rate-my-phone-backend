import json
import requests as r

from logging import Logger
from typing import Dict, List, Optional
from flask import Response, current_app, jsonify
from cachetools import TTLCache, cached
from device.model.device import Device, DeviceResponse
from . import DEVICE

logger = Logger(__name__)

@DEVICE.route('/device')
def get_all_devices_by_brand() -> Response:
  """Endpoint for getting all devices

  Returns:
      Response: list of devices sorted by brands
  """
  devices = get_device_list_by_brands()
  return jsonify(devices)


@DEVICE.route('/device/<brand_key>')
def get_device_by_brand(brand_key: str) -> Response:
  """Endpoint for getting all devices by brand

  Args:
      brand_key (str): brand key i.e.: nokia

  Returns:
      Dict: all data from gsm arena api with devices sorted by brand
  """
  logger.info(f"Getting devices by brand!")
  devices = get_device_list_by_brands()
  return jsonify(get_devices_by_key(brand_key, devices))


@DEVICE.route('/device/recommended')
def get_recommended_devices() -> Response:
  """Getting recommended devices by GSMARENA

  Returns:
      Response: Response with json of recommended listings
  """
  recommended = get_recommended_devices()
  return jsonify(recommended)


@DEVICE.route('/device/details/<device_key>', methods=['GET'])
def get_details_of_device(device_key: str) -> Response:
  """Getting device detail from with api key

  Args:
      device_key (str): device key

  Returns:
      Dict: dict with all of the data from GSM ARENA API
  """
  device_detail = get_device_detail_from_api(device_key)
  return jsonify(device_detail)


def get_devices_by_key(brand_key: str, brands: List['DeviceResponse']) -> Optional['Device']:
  """Get device by key

  Returns:
      Optional['Device']: device object
  """
  for device in brands:
    if device.key == brand_key:
      return device.device_list
  return None


def parse_to_device_dataclass(device_list: List) -> List['Device']:
  """Function for parsing json object to device dataclass

  Returns:
      List['Device']: list of parsed devices
  """
  return [Device(**device) for device in device_list]


def parse_response(data: List[Dict]) -> List[DeviceResponse]:
  """Parse response from api to datclas

  Args:
      data (List[Dict]): get list of dicts with response

  Returns:
      List[DeviceResponse]: getting devices with brands name
  """
  data_list = []
  for res in data:
    devices = parse_to_device_dataclass(res.get('device_list', []))
    res['device_list'] = devices
    data_list.append(DeviceResponse(**res))
  return data_list


@cached(cache=TTLCache(maxsize=1000, ttl=3000))
def get_device_list_by_brands() -> List[DeviceResponse]:
  """Function for getting parsed response from GSMARENA API

  Returns:
      List[DeviceResponse]: Data with responses
  """
  logger.info("Getting data from GSM ARENA API")
  GSM_ARENA_API_URL: str = current_app.config.get('GSM_ARENA_API_URL', '')
  req = r.get(GSM_ARENA_API_URL, {'route': 'device-list'})
  data: Dict = req.json()
  json_data = data.get('data', {})
  return parse_response(json_data)


def get_device_detail_from_api(device_key: str) -> Dict:
  """Function for getting devices details

  Args:
      device_key (str): key for searching in api i.e.: samsung_galaxy_s21_5g-10626

  Returns:
      Dict: device detail
  """
  GSM_ARENA_API_URL: str = current_app.config.get('GSM_ARENA_API_URL', '')
  req = r.post(GSM_ARENA_API_URL, json.dumps({'route': 'device-detail', 'key': device_key}))
  data: Dict = req.json()
  return data.get('data', {})


def get_recommended_devices() -> Dict:
  """Getting recommended listings from gsm arena

  Returns:
      Dict: dict with all data
  """
  GSM_ARENA_API_URL: str = current_app.config.get('GSM_ARENA_API_URL', '')
  req = r.get(f"{GSM_ARENA_API_URL}?route=recommended")
  data: Dict = req.json()
  return data.get('data', {})
