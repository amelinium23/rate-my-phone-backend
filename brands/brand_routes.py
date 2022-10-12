from typing import Any, Dict, List, Optional
from flask import Response, jsonify, request, current_app
from brands import BRANDS
from .model.brand import Brand

from google.cloud.firestore import Client as FirestoreClient


@BRANDS.route("/", methods=["GET"])
def get_brand_list() -> Response:
    try:
        db: FirestoreClient = current_app.config.get("FIRESTORE")
        args: Dict[str, str] = request.args.to_dict()
        page_number: int = int(args.get("page_number", 1))
        page_size: int = int(args.get("page_size", 20))
        brands: List[Brand] = _get_brand_list(db)
        sort_mode: str = args.get("sort_mode", "ascending")
        start_index: int = (page_number - 1) * page_size
        end_index: int = start_index + page_size
        sorted_brands: List[Brand] = _get_result_brand_list(
            start_index, end_index, sort_mode, brands
        )
        result: Dict[str, Any] = {
            "brands": sorted_brands,
            "total_pages": len(brands),
        }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)


@BRANDS.route("/k", methods=["GET"])
def get_brand_key() -> Response:
    try:
        data: Dict[str, Any] = request.args.to_dict()
        db: FirestoreClient = current_app.config.get("FIRESTORE")
        key: str = data.get("key", "")
        brands: List["Brand"] = _get_brand_list(db)
        return jsonify(_get_brand_by_key(brands, key))
    except Exception as e:
        return Response(str(e), status=500)


def _get_brand_by_key(brands: List["Brand"], key: str) -> Optional["Brand"]:
    for brand in brands:
        if brand.key == key:
            return brand
    return None


def _get_brand_list(db: FirestoreClient) -> List["Brand"]:
    brands = db.collection("brands").document("brands").get().to_dict()
    real_brands = brands.get("brands", [])
    return [Brand(**brand) for brand in real_brands]


def _get_result_brand_list(
    start_index: int, end_index: int, sort_mode: str, brands: List["Brand"]
) -> List["Brand"]:
    return sorted(
        brands, key=lambda brand: brand.brand_name, reverse=sort_mode == "descending"
    )[start_index:end_index]
