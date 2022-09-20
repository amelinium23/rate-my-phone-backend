from typing import Any, Dict, List, Optional
from flask import Response, jsonify, request
from brands import BRANDS
from .model.brand import Brand
from cachetools import TTLCache, cached
from utils.gsm_arena_utils import get_from_gsm_arena


@BRANDS.route("/", methods=["GET"])
def get_brand_list() -> Response:
    try:
        args: Dict[str, str] = request.args.to_dict()
        page_number: int = int(args.get("page_number", 1))
        page_size: int = int(args.get("page_size", 20))
        brands: List[Brand] = _get_brand_list()
        start_index: int = (page_number - 1) * page_size
        end_index: int = start_index + page_size
        result: Dict[str, Any] = {
            "brands": brands[start_index:end_index],
            "total_pages": len(brands),
        }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@BRANDS.route("/k", methods=["GET"])
def get_brand_key() -> Response:
    try:
        data: Dict[str, Any] = request.args.to_dict()
        key: str = data.get("key", "")
        brands: List["Brand"] = _get_brand_list()
        return jsonify(_get_brand_by_key(brands, key))
    except Exception as e:
        return Response(str(e), status=500)


def _get_brand_by_key(brands: List["Brand"], key: str) -> Optional["Brand"]:
    for brand in brands:
        if brand.key == key:
            return brand
    return None


def _parse_brands(data: Dict[str, Any]) -> List[Brand]:
    return [Brand(**brand) for brand in data.get("data", {})]


@cached(cache=TTLCache(maxsize=1000, ttl=14400))
def _get_brand_list() -> List["Brand"]:
    data: Dict = get_from_gsm_arena({"route": "brand-list"})
    brands: List["Brand"] = _parse_brands(data)
    return brands
