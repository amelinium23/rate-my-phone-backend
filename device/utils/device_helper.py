from typing import Dict, List, Any
from device.utils.response_parser import parse_response
from utils.gsm_arena_utils import post_to_gsm_arena
from cachetools import TTLCache, cached
from device.model.device import DeviceResponse
from utils.gsm_arena_utils import get_from_gsm_arena, post_to_gsm_arena


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_device_list_by_brands() -> List[DeviceResponse]:
    data: Dict = get_from_gsm_arena({"route": "device-list"})
    json_data = data.get("data", {})
    return parse_response(json_data)


def get_device_detail_from_api(device_key: str) -> Dict[str, Any]:
    data: Dict = post_to_gsm_arena(
        {"route": "device-detail", "key": device_key})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_search_result_from_api(query: str) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena(
        {"route": "search", "query": query})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_recommended_devices_from_api() -> List[Dict[str, Any]]:
    data: Dict = get_from_gsm_arena({}, "?route=recommended")
    return _parse_recommended_devices_to_list(data.get("data", {}))


def get_comparison_of_devices(device_ids: List[int]) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena(
        {"route": "compare", "device_ids": ",".join(
            str(x) for x in device_ids)}
    )
    return data.get("data", {})


def _parse_recommended_devices_to_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        value
        for key, value in data.items()
        if key in ["recommended_1", "recommended_2"]
    ]


def count_phones(responses: List["DeviceResponse"]) -> int:
    return sum([len(response.device_list) for response in responses])
