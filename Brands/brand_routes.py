from ast import Dict, List
from flask import Blueprint, Response
import json
import requests as r

brands = Blueprint('brands', __name__)

GSM_ARENA_API_URL = 'https://script.google.com/macros/s/AKfycbxNu27V2Y2LuKUIQMK8lX1y0joB6YmG6hUwB1fNeVbgzEh22TcDGrOak03Fk3uBHmz-/exec'

@brands.route('/brands')
def get_device_list() -> Response:
    req = r.get(GSM_ARENA_API_URL, {'route': 'brand-list'})
    data: Dict = req.json()
    brands: List['Brand'] = data.get('data', {})
    return Response(json.dumps(brands), status=req.status_code, content_type=req.headers.get('content-type'))