import json
from device.utils.response_parser import get_devices_by_key, parse_response
from . import DEVICE
from typing import Dict, List, Any
from flask import Response, jsonify, request
from cachetools import TTLCache, cached
from device.model.device import DeviceResponse
from utils.gsm_arena_utils import get_from_gsm_arena, post_to_gsm_arena


@DEVICE.route("/")
def get_all_devices_by_brand() -> Response:
    try:
        args: Dict[str, str] = request.args.to_dict()
        page_number: int = int(args.get("page_number", 1))
        page_size: int = int(args.get("page_size", 10))
        start_index: int = (page_number - 1) * page_size
        end_index: int = start_index + page_size
        devices = get_device_list_by_brands()
        result = {
            "data": devices[start_index:end_index],
            "total": len(devices),
            "totalPhones": _count_phones(devices),
        }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/brand", methods=["GET"])
def get_device_by_brand() -> Response:
    try:
        params: Dict[str, str] = request.args.to_dict()
        brand_key: str = params.get("brand_key", "")
        devices = get_device_list_by_brands()
        devices_from_brand = get_devices_by_key(brand_key, devices)
        result = {
            "data": devices_from_brand,
            "totalPhones": _count_phones(devices),
            "total": len(devices_from_brand) if devices_from_brand else 1 }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/recommended")
def get_recommended_devices() -> Response:
    try:
        recommended = _get_recommended_devices()
        return jsonify(recommended)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/details", methods=["GET"])
def get_details_of_device() -> Response:
    try:
        params: Dict[str, str] = request.args.to_dict()
        device_key: str = params.get("device_key", "")
        device_detail = get_device_detail_from_api(device_key)
        return jsonify(device_detail)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/search", methods=["GET"])
def get_search_result() -> Response:
    try:
        params: Dict[str, str] = request.args.to_dict()
        query: str = params.get("query", "")
        return jsonify(_get_search_result(query))
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/comparison", methods=["POST"])
def get_comparison_result() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        device_ids: List[int] = data.get("device_ids", [])
        comparison = _get_comparison_of_devices(device_ids)
        return jsonify(comparison)
    except Exception as e:
        return Response(str(e), status=500)


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_device_list_by_brands() -> List[DeviceResponse]:
    data: Dict = get_from_gsm_arena({"route": "device-list"})
    json_data = data.get("data", {})
    return parse_response(json_data)


def get_device_detail_from_api(device_key: str) -> Dict[str, Any]:
    data: Dict = post_to_gsm_arena({"route": "device-detail", "key": device_key})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def _get_search_result(query: str) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena({"route": "search", "query": query})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def _get_recommended_devices() -> List[Dict[str, Any]]:
    data: Dict = get_from_gsm_arena({}, "?route=recommended")
    return _parse_recommended_devices_to_list(data.get("data", {}))


def _get_comparison_of_devices(device_ids: List[int]) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena(
        {"route": "compare", "device_ids": ",".join(str(x) for x in device_ids)}
    )
    return data.get("data", {})


def _parse_recommended_devices_to_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        value
        for key, value in data.items()
        if key in ["recommended_1", "recommended_2"]
    ]


def _count_phones(responses: List["DeviceResponse"]) -> int:
    return sum([len(response.device_list) for response in responses])
