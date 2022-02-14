from typing import Dict, List
from flask import Response, current_app, jsonify
import requests as r
from .model.brand import Brand
from cachetools import TTLCache, cached

from . import BRANDS


@BRANDS.route('/brands', methods=['GET'])
def get_brand_list() -> Response:
    brands = get_brand_list()
    return jsonify(brands)


@BRANDS.route('/brands/<key>', methods=['GET'])
def get_brand_key(key: str) -> Response:
    brands: List['Brand'] = get_brand_list()
    return jsonify(get_brand_by_key(brands, key))


def get_brand_by_key(brands: List['Brand'], key: str) -> 'Brand':
    for brand in brands:
        if brand.key == key:
            return brand
    return None


@cached(cache=TTLCache(maxsize=1000, ttl=3000))
def get_brand_list() -> List['Brand']:
    GSM_ARENA_API_URL = current_app.config.get('GSM_ARENA_API_URL', '')
    req = r.get(GSM_ARENA_API_URL, {'route': 'brand-list'})
    data: Dict = req.json()
    brands: List['Brand'] = [Brand(**brand) for brand in data.get('data', {})]
    return brands
