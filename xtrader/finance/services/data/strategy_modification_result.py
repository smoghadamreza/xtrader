
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Optional

class StrategyAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ERROR = "error"

@dataclass
class StrategyModificationResult:
    """
    Encapsulates the outcome of a create/update/delete operation.

    - action: StrategyAction (CREATE|UPDATE|DELETE|ERROR)
    - id: strategy id (may be None for error)
    - redirect/status/message: legacy fields kept for compatibility when needed
    """
    action: StrategyAction
    id: Optional[int] = None
    status: Optional[int] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        # convert enum to its value for JSON serialization
        d = asdict(self)
        d["action"] = self.action.value
        return d
