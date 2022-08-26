import json
from typing import Any
from dataclasses import is_dataclass, asdict


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> Any:
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)
