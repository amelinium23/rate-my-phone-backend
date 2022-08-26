import json
import requests as r
from typing import Any, Dict

GSM_ARENA_API_URL = "https://script.google.com/macros/s/AKfycbxNu27V2Y2LuKUIQMK8lX1y0joB6YmG6hUwB1fNeVbgzEh22TcDGrOak03Fk3uBHmz-/exec"


def get_from_gsm_arena(params: Dict[str, str], search: str = "") -> Dict[str, Any]:
    req = r.get(f"{GSM_ARENA_API_URL}{search}", params)
    return req.json()


def post_to_gsm_arena(params: Dict[str, str]) -> Dict[str, Any]:
    req = r.post(GSM_ARENA_API_URL, data=json.dumps(params))
    return req.json()
