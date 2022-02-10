from ast import Dict, List
from flask import Blueprint, Response, current_app
import json
import requests as r
from brands.model.brand import Brand
from utils.json_utils import EnhancedJSONEncoder

brands = Blueprint('brands', __name__)

@brands.route('/brands')
def get_device_list() -> Response:
    GSM_ARENA_API_URL = current_app.config.get('GSM_ARENA_API_URL', '')
    req = r.get(GSM_ARENA_API_URL, {'route': 'brand-list'})
    data: Dict = req.json()
    brands: List[Brand] = [Brand(**brand) for brand in data.get('data', {})]
    return Response(json.dumps(brands, cls=EnhancedJSONEncoder),
                    status=req.status_code,
                    content_type=req.headers.get('content-type'))
