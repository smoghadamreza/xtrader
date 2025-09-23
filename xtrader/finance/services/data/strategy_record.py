from dataclasses import dataclass, asdict
from typing import Union, Dict


@dataclass
class StrategyRecord:
    id: int
    name: str

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return asdict(self)
