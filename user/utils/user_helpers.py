from typing import Dict, Any
from device.model.device import Device
from user.utils.firebase_util import (
    get_user_mapping,
    get_user_device,
    update_device_of_user,
)
from firebase_admin.auth import get_user, create_user
from user.model.user import User


def get_user_information(uid: str) -> User:
    user = get_user(uid)
    user_device = get_user_device(uid)
    user_mapping = get_user_mapping(user)
    return User(**user_mapping, device=user_device)


def create_user_in_database(data: Dict[str, Any]) -> User:
    user = create_user(**data)
    user_instance = User(**get_user_mapping(user), device=None)
    return user_instance
