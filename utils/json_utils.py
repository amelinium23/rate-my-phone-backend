import dataclasses, json
from typing import Any

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
