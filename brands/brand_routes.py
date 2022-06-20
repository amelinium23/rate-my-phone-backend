from typing import Dict, List
from flask import Response, jsonify
from brands import BRANDS
from .model.brand import Brand
from cachetools import TTLCache, cached
from utils.gsm_arena_utils import get_from_gsm_arena


@BRANDS.route('/', methods=['GET'])
def _get_brand_list() -> Response:
  brands = _get_brand_list()
  return jsonify(brands)


@BRANDS.route('/<key>', methods=['GET'])
def get_brand_key(key: str) -> Response:
  brands: List['Brand'] = _get_brand_list()
  return jsonify(_get_brand_by_key(brands, key))


def _get_brand_by_key(brands: List['Brand'], key: str) -> 'Brand':
  for brand in brands:
    if brand.key == key:
      return brand
  return None


def _parse_brands(data: Dict) -> List[Brand]:
    return [Brand(**brand) for brand in data.get('data', {})]


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def _get_brand_list() -> List['Brand']:
  data: Dict = get_from_gsm_arena({'route': 'brand-list'})
  brands: List['Brand'] = _parse_brands(data)
  return brands
