from dataclasses import asdict
from firebase_admin.auth import UserRecord
from typing import Dict

from google.cloud.firestore import Client as FirestoreClient
from device.model.device import Device
from flask import current_app


def get_user_mapping(user: UserRecord) -> Dict[str, str]:
    return {
        "uid": user.uid,
        "email": user.email,
        "display_name": user.display_name,
        "photo_url": user.photo_url,
    }


def update_device_of_user(uid: str, device: Device) -> None:
    db: FirestoreClient = current_app.config.get("FIRESTORE", None)
    db.collection("device").document(uid).set({"device": asdict(device)})


def get_user_device(uid: str) -> Device:
    db: FirestoreClient = current_app.config.get("FIRESTORE", None)
    doc = db.collection("device").document(uid).get().to_dict()
    return Device(**doc.get("device", {}))


def delete_user_device(uid: str) -> None:
    db: FirestoreClient = current_app.config.get("FIRESTORE", None)
    db.collection("device").document(uid).delete()
