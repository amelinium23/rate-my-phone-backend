import json

from typing import Any, Dict
from allegro.utils.allegro_authorization import get_access_token
from allegro.utils.allegro_api_utils import get_categories, get_categories_by_parent_id, search_listings_in_allegro
from . import ALLEGRO
from flask import Response, jsonify, request


@ALLEGRO.route('/')
def search_listings_in_allegro() -> str:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    token: Dict[str, Any] = get_access_token()
    device_name: str = data.get('device_name', '')
    listings = search_listings_in_allegro(device_name, token.get('access_token', ''))
    return jsonify(listings)
  except Exception as e:
    return str(e)


@ALLEGRO.route('/categories', methods=['GET'])
def get_categories_from_allegro() -> Response:
  try:
    token: Dict[str, Any] = get_access_token()
    categories = get_categories(token.get('access_token', ''))
    return jsonify(categories)
  except Exception as e:
    return Response(str(e), status=500)


@ALLEGRO.route('/categories/parent', methods=['GET'])
def get_category_by_parent_id() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    parent_id: str = data.get('parent_id', '')
    token: Dict[str, Any] = get_access_token()
    categories = get_categories_by_parent_id(token.get('access_token', ''), parent_id)
    return jsonify(categories)
  except Exception as e:
    return Response(str(e), status=500)
