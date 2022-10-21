from dataclasses import asdict
from typing import Dict, List
from google.cloud.firestore import Client as FirestoreClient
from flask import Flask
from device.model.device import DeviceResponse
from device.utils.response_parser import parse_response
from utils.gsm_arena_utils import get_from_gsm_arena


def device_task(app: Flask) -> None:
    with app.app_context():
        db: FirestoreClient = app.config.get("FIRESTORE")
        devices: List[DeviceResponse] = get_device_list_by_brands()
        parsed_devices = [asdict(device) for device in devices]
        db.collection("devices").document("devices").set({"devices": parsed_devices})


def get_device_list_by_brands() -> List[DeviceResponse]:
    data: Dict = get_from_gsm_arena({"route": "device-list"})
    json_data = data.get("data", {})
    return parse_response(json_data)
