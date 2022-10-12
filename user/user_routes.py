import json
from device.model.device import Device

from logging import getLogger
from . import USER
from typing import Any, Dict
from flask import Response, jsonify, request
from user.utils.firebase_util import (
    delete_user_device,
    get_user_device,
    get_user_mapping,
    update_device_of_user,
)
from firebase_admin.auth import get_user, create_user, update_user, delete_user
from user.model.user import User

logger = getLogger(__name__)


@USER.route("/", methods=["GET"])
def get_user_by_id() -> Response:
    try:
        data: Dict[str, Any] = request.args.to_dict()
        uid = data.get("uid")
        assert uid is not None, "uid param is required"
        user = get_user(uid)
        user_device = get_user_device(uid)
        user_mapping = get_user_mapping(user)
        user_instance = User(**user_mapping, device=user_device)
        logger.info(f"[USER]: Get user with uid {user.uid}")
        return jsonify(user_instance)
    except Exception as e:
        return Response(str(e), status=500)


@USER.route("/", methods=["POST"])
def create_new_user() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        user = create_user(**data)
        device = Device(**data.get("device", {}))
        user_instance = User(**get_user_mapping(user), device=device)
        logger.info(f"[USER]: Created new user with uid {user_instance.uid}")
        return jsonify(user_instance)
    except Exception as e:
        return Response(str(e), status=500)


@USER.route("/", methods=["PUT"])
def edit_user() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        uid = data.get("uid")
        assert uid is not None, "uid param is required"
        rest_data = {k: v for k, v in data.items() if k != "uid"}
        user = update_user(uid, **rest_data)
        device = get_user_device(uid)
        user_instance = User(**get_user_mapping(user), device=device)
        logger.info(f"[USER]: Edited user with uid {user_instance.uid}")
        return jsonify(user_instance)
    except Exception as e:
        return Response(str(e), status=500)


@USER.route("/", methods=["DELETE"])
def delete_firebase_user() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        uid = data.get("uid")
        assert uid is not None, "uid param is required"
        delete_user(uid)
        delete_user_device(uid)
        logger.info(f"[USER]: Deleted user with uid {uid}")
        return Response(f"Deleted user with uid: {uid}", status=200)
    except Exception as e:
        return Response(str(e), status=500)


@USER.route("/device", methods=["PUT"])
def edit_user_device() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        uid = data.get("uid", "")
        new_device = Device(**data.get("device", {}))
        update_device_of_user(uid, new_device)
        logger.info(f"[USER]: Edited user device with uid {uid}")
        return Response(f"Updated user {uid} device", status=200)
    except Exception as e:
        return Response(str(e), status=500)
