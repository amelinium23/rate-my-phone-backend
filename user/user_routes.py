import json
from . import USER
from typing import Any, Dict
from flask import Response, jsonify, request
from user.utils.firebase_util import get_user_mapping
from firebase_admin.auth import get_user, create_user, update_user, delete_user
from user.model.user import User


@USER.route('/user', methods=['GET'])
def get_user_by_id() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    user = get_user(data.get('uid', ''))
    user_instance = User(**get_user_mapping(user))
    return jsonify(user_instance)
  except Exception as e:
    return Response(str(e), status=500)


@USER.route('/user', methods=['POST'])
def create_new_user() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    user = create_user(**data)
    user_instance = User(**get_user_mapping(user))
    return jsonify(user_instance)
  except Exception as e:
    return Response(str(e), status=500)


@USER.route('/user', methods=['PUT'])
def edit_user() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    uid = data.get('uid')
    assert uid is not None, 'uid param is required'
    rest_data = {k: v for k, v in data.items() if k != 'uid'}
    user = update_user(uid, **rest_data)
    user_instance = User(**get_user_mapping(user))
    return jsonify(user_instance)
  except Exception as e:
    return Response(str(e), status=500)


@USER.route('/user', methods=['DELETE'])
def delete_firebase_user() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    uid = data.get('uid')
    assert uid is not None, 'uid param is required'
    delete_user(uid)
    return Response(f"Deleted user with uid: {uid}", status=200)
  except Exception as e:
    return Response(str(e), status=500)
