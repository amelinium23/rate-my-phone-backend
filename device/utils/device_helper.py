from typing import Dict, List, Any
from utils.gsm_arena_utils import post_to_gsm_arena
from cachetools import TTLCache, cached
from device.model.device import DeviceResponse
from utils.gsm_arena_utils import get_from_gsm_arena, post_to_gsm_arena
from google.cloud.firestore import Client as FirestoreClient
from device.utils.price_helper import parse_string_price_to_float


def get_device_list_by_brands(db: FirestoreClient) -> List[DeviceResponse]:
    devices = db.collection("devices").document("devices").get().to_dict()
    real_devices = devices.get("devices", [])
    devices_data = [DeviceResponse(**response) for response in real_devices]
    filtered_devices = filter(lambda x: x.brand_name != "", devices_data)
    return list(filtered_devices)


def get_device_detail_from_api(device_key: str) -> Dict[str, Any]:
    data: Dict = post_to_gsm_arena({"route": "device-detail", "key": device_key})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_search_result_from_api(query: str) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena({"route": "search", "query": query})
    return data.get("data", {})


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def get_recommended_devices_from_api() -> List[Dict[str, Any]]:
    data: Dict = get_from_gsm_arena({}, "?route=recommended")
    return _parse_recommended_devices_to_list(data.get("data", {}))


def get_comparison_of_devices(device_ids: List[int]) -> Dict[str, Any]:
    data: Dict[str, Any] = post_to_gsm_arena(
        {"route": "compare", "device_id": ",".join(str(x) for x in device_ids)}
    )
    return data.get("data", {})


def get_comparison_of_price(device_key: str) -> Dict[str, Any]:
    data: Dict[str, Any] = get_device_detail_from_api(device_key)
    prices_object: Dict[str, List[Dict[str, Any]]] = data.get("prices", {})
    result: Dict[str, Dict[str, Any]] = {}
    for key, value in prices_object.items():
        if value:
            prices = [price.get("price", "") for price in value if price.get("price")]
            currency = [price.replace("\u200b", "") for price in prices]
            real_prices = [parse_string_price_to_float(price) for price in prices]
            every_price = {
                "min": min(real_prices),
                "max": max(real_prices),
                "average": round(sum(real_prices) / len(real_prices), 3),
                "currency": currency[0][0],
            }
            result[key] = every_price
    return result


def sort_devices(devices, sort_mode: str) -> List[DeviceResponse]:
    for brand in devices:
        brand.device_list = sorted(
            brand.device_list,
            key=lambda x: x["device_name"],
            reverse=sort_mode == "descending",
        )
    return sorted(
        devices, key=lambda x: x.brand_name, reverse=sort_mode == "descending"
    )


def _parse_recommended_devices_to_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        value
        for key, value in data.items()
        if key in ["recommended_1", "recommended_2"]
    ]


def count_phones(responses: List["DeviceResponse"]) -> int:
    return sum([len(response.device_list) for response in responses])
