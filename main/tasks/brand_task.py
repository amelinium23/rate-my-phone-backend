from dataclasses import asdict
from typing import Any, Dict, List
from flask import Flask
from brands.model.brand import Brand
from google.cloud.firestore import Client as FirestoreClient
from utils.gsm_arena_utils import get_from_gsm_arena
from logging import getLogger

logger = getLogger(__name__)


def brand_task(app: Flask) -> None:
    with app.app_context():
        logger.info("[TASK] Starting brand task")
        db: FirestoreClient = app.config.get("FIRESTORE")
        brands: List[Brand] = _get_brand_list()
        dicts_brands: List[Dict[str, Any]] = [
            asdict(brand) for brand in brands if brand.brand_name != ""
        ]
        db.collection("brands").document("brands").set({"brands": dicts_brands})


def _parse_brands(data: Dict[str, Any]) -> List[Brand]:
    return [Brand(**brand) for brand in data.get("data", {})]


def _get_brand_list() -> List["Brand"]:
    data: Dict = get_from_gsm_arena({"route": "brand-list"})
    brands: List["Brand"] = _parse_brands(data)
    return brands
