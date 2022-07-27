from typing import Any, Dict
from allegro.utils.allegro_authorization import get_access_token
from allegro.utils.allegro_api_utils import get_categories, get_categories_by_parent_id, search_listings_in_allegro, get_categories_by_id
from . import ALLEGRO
from flask import Response, jsonify, request


@ALLEGRO.route('/listings', methods=['GET'])
def search_listings() -> Response:
  try:
    data: Dict[str, Any] = request.args.to_dict()
    token: Dict[str, Any] = get_access_token()
    device_name: str = data.get('device_name', '')
    listings = search_listings_in_allegro(device_name, token.get('access_token', ''))
    return jsonify(listings)
  except Exception as e:
    return Response(str(e), status=500)


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
    data: Dict[str, Any] = request.args.to_dict()
    parent_id: str = data.get('parent_id', '')
    token: Dict[str, Any] = get_access_token()
    categories = get_categories_by_parent_id(token.get('access_token', ''), parent_id)
    return jsonify(categories)
  except Exception as e:
    return Response(str(e), status=500)


@ALLEGRO.route('/categories/id', methods=['GET'])
def get_category_by_id() -> Response:
  try:
    data: Dict[str, Any] = request.args.to_dict()
    category_id: str = data.get('category_id', '')
    token: Dict[str, Any] = get_access_token()
    categories = get_categories_by_id(token.get('access_token', ''), category_id)
    return jsonify(categories)
  except Exception as e:
    return Response(str(e), status=500)
