from typing import Dict, List
from flask import Blueprint, Response, current_app
import json
import requests as r
from brands.model.brand import Brand
from utils.json_utils import EnhancedJSONEncoder

brands = Blueprint('brands', __name__)


@brands.route('/brands', methods=['GET'])
def get_brand_list() -> Response:
    GSM_ARENA_API_URL = current_app.config.get('GSM_ARENA_API_URL', '')
    req = r.get(GSM_ARENA_API_URL, {'route': 'brand-list'})
    data: Dict = req.json()
    brands: List[Brand] = [Brand(**brand) for brand in data.get('data', {})]
    return Response(json.dumps(brands, cls=EnhancedJSONEncoder),
                    status=req.status_code,
                    content_type=req.headers.get('content-type'))


@brands.route('/brands/<key>', methods=['GET'])
def get_brand_key(key: str) -> Response:
    GSM_ARENA_API_URL = current_app.config.get('GSM_ARENA_API_URL', '')
    req = r.get(GSM_ARENA_API_URL, {'route': 'brand-list'})
    data: Dict = req.json()
    brands: List['Brand'] = [Brand(**brand) for brand in data.get('data', {})]
    return Response(json.dumps(get_brand_by_key(brands, key), cls=EnhancedJSONEncoder))


def get_brand_by_key(brands: List['Brand'], key: str) -> 'Brand':
    for brand in brands:
        if brand.key == key:
            return brand
    return None
