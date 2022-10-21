import json
from device.utils.device_helper import (
    count_phones,
    get_comparison_of_devices,
    get_comparison_of_price,
    get_recommended_devices_from_api,
    get_device_detail_from_api,
    get_device_list_by_brands,
    sort_devices,
)
from device.utils.response_parser import get_devices_by_key
from . import DEVICE
from typing import Dict, List, Any
from flask import Response, jsonify, request, current_app
from google.cloud.firestore import Client as FirestoreClient


@DEVICE.route("/")
def get_all_devices_by_brand() -> Response:
    try:
        args: Dict[str, str] = request.args.to_dict()
        db: FirestoreClient = current_app.config.get("FIRESTORE")
        page_number = args.get("page_number")
        page_size = args.get("page_size")
        sort_mode = args.get("sort_mode", "ascending")
        devices = get_device_list_by_brands(db)
        sorted_devices = sort_devices(devices, sort_mode)
        result = {
            "data": sorted_devices,
            "total": len(devices),
            "totalPhones": count_phones(devices),
        }
        if page_size and page_number and sort_mode:
            start_index: int = (int(page_number) - 1) * int(page_size)
            end_index: int = start_index + int(page_size)
            result = {
                "data": sorted_devices[start_index:end_index],
                "total": len(devices),
                "totalPhones": count_phones(devices),
            }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/brand", methods=["GET"])
def get_device_by_brand() -> Response:
    try:
        db: FirestoreClient = current_app.config.get("FIRESTORE")
        params: Dict[str, str] = request.args.to_dict()
        brand_key: str = params.get("brand_key", "")
        devices = get_device_list_by_brands(db)
        devices_from_brand = get_devices_by_key(brand_key, devices)
        result = {
            "data": devices_from_brand,
            "totalPhones": count_phones(devices),
            "total": len(devices_from_brand) if devices_from_brand else 1,
        }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/recommended")
def get_recommended_devices() -> Response:
    try:
        recommended = get_recommended_devices_from_api()
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
        return jsonify(get_search_result(query))
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/comparison", methods=["POST"])
def get_comparison_result() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        device_ids: List[int] = data.get("device_ids", [])
        comparison = get_comparison_of_devices(device_ids)
        return jsonify(comparison)
    except Exception as e:
        return Response(str(e), status=500)


@DEVICE.route("/price", methods=["GET"])
def get_prices_of_phone() -> Response:
    try:
        params: Dict[str, str] = request.args.to_dict()
        device_key: str = params.get("device_key", "")
        return jsonify(get_comparison_of_price(device_key))
    except Exception as e:
        return Response(str(e), status=500)
