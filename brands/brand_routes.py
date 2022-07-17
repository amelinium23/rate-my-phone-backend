import json
from typing import Any, Dict, List, Optional
from flask import Response, jsonify, request
from brands import BRANDS
from .model.brand import Brand
from cachetools import TTLCache, cached
from utils.gsm_arena_utils import get_from_gsm_arena


@BRANDS.route('/', methods=['GET'])
def get_brand_list() -> Response:
  try:
    brands = _get_brand_list()
    return jsonify(brands)
  except Exception as e:
    return Response(str(e), status=500)


@BRANDS.route('/', methods=['GET'])
def get_brand_key() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    key: str = data.get('key', '')
    brands: List['Brand'] = _get_brand_list()
    return jsonify(_get_brand_by_key(brands, key))
  except Exception as e:
    return Response(str(e), status=500)


def _get_brand_by_key(brands: List['Brand'], key: str) -> Optional['Brand']:
  for brand in brands:
    if brand.key == key:
      return brand
  return None


def _parse_brands(data: Dict[str, Any]) -> List[Brand]:
  return [Brand(**brand) for brand in data.get('data', {})]


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def _get_brand_list() -> List['Brand']:
  data: Dict = get_from_gsm_arena({'route': 'brand-list'})
  brands: List['Brand'] = _parse_brands(data)
  return brands
