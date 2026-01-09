from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class MartingaleStrategyConfig:
    """
    Configuration parameters for a Martingale-based trading strategy.

    This strategy involves re-buying on price drops (stop-loss trigger)
    and exiting on a price increase (take-profit trigger).

    Attributes:
        symbol_id: The trading pair or instrument identifier.
        initial_capital: The initial capital allocated for trading.
        take_profit_factor: The profit-taking threshold (as a fraction of the initial entry price).
        stop_loss_factor: The stop-loss threshold (as a fraction of the initial entry price).
    """

    symbol_id: str = "IRO1KAVR0001"
    initial_capital: float = 10_000_000
    take_profit_factor: float = 0.3
    stop_loss_factor: float = 0.1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MartingaleStrategyConfig":
        """
        Create a MartingaleStrategyConfig instance from a dictionary,
        ignoring unexpected keys.
        """
        # Using a list comprehension for better readability and a direct map
        # between the dictionary keys and the dataclass fields.
        config_data = {
            field.name: data[field.name]
            for field in cls.__dataclass_fields__.values()
            if field.name in data
        }
        return cls(**config_data)
