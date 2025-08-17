from dataclasses import dataclass, asdict
from typing import List, Dict, Any

from finance.exchange.data import SymbolInfo, MarketDepth


@dataclass
class OrderBookLevel:
    bid_price: float
    bid_quantity: float
    ask_price: float
    ask_quantity: float

    def to_dict(self) -> dict:
        return {
            "bp": self.bid_price,
            "bq": self.bid_quantity,
            "ap": self.ask_price,
            "aq": self.ask_quantity,
        }

@dataclass
class StockWatchInfo:
    instrument_name: str
    company_name: str
    depth: List[OrderBookLevel]

    @classmethod
    def load(
        cls, symbol_info: SymbolInfo, market_depth: MarketDepth
    ) -> "StockWatchInfo":
        """
        Create a StockWatchInfo instance from a dictionary.
        """
        order_book_level_length = min(
            len(market_depth.bids),
            len(market_depth.asks)
        )
        depth_list = [
            OrderBookLevel(
                bid_price=market_depth.bids[idx].price,
                bid_quantity=market_depth.bids[idx].quantity,
                ask_price=market_depth.asks[idx].price,
                ask_quantity=market_depth.asks[idx].quantity,
            )
            for idx in range(order_book_level_length)
        ]
        return cls(
            instrument_name=symbol_info.symbol,
            company_name=symbol_info.base_asset,
            depth=depth_list
        )

    def to_dict(self, depth_limit: int) -> Dict[str, Any]:
        """
        Convert the dataclass instance to a dictionary.
        """
        return {
            "InstrumentName": self.instrument_name,
            "CompanyName": self.company_name,
            "depth": [
                order_book_level.to_dict()
                for order_book_level in self.depth
            ]
        }
