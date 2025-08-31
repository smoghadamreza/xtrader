from typing import List, Dict, Any, Optional

from dataclasses import dataclass, asdict
from finance.services.exchange.constants.binance import BinanceResponseKeys, BinanceResponseValues

@dataclass
class LotFilter:
    """
    Represents a LOT_SIZE filter from Binance exchange info.

    Fields:
    - filter_type: Should always be "LOT_SIZE"
    - min_quantity: Minimum quantity allowed per order
    - max_quantity: Maximum quantity allowed per order
    - step_size: Step size for quantity increments
    """
    filter_type: str
    min_quantity: float
    max_quantity: float
    step_size: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LotFilter":
        return cls(
            filter_type=data[BinanceResponseKeys.FILTER_TYPE],
            min_quantity=float(data[BinanceResponseKeys.MIN_QUANTITY]),
            max_quantity=float(data[BinanceResponseKeys.MAX_QUANTITY]),
            step_size=float(data[BinanceResponseKeys.STEP_SIZE]),
        )


@dataclass
class SymbolInfo:
    """
    Represents metadata for a trading symbol on Binance.

    Fields:
    - symbol: Trading symbol (e.g., BTCUSDT)
    - status: Trading status
    - base_asset, quote_asset: Base and quote asset symbols
    - precision fields: Decimal precision for trading/commission
    - supported_order_types: Allowed order types
    - boolean flags for feature support
    - lot_filter: Only the single LOT_SIZE filter
    - permissions, STP modes: Various optional config details
    """

    symbol: str
    status: str
    base_asset: str
    base_asset_precision: int
    quote_asset: str
    quote_precision: int
    quote_asset_precision: int
    base_commission_precision: int
    quote_commission_precision: int
    supported_order_types: List[str]
    is_iceberg_order_allowed: bool
    is_one_cancels_other_allowed: bool
    is_one_triggers_other_allowed: bool
    is_quote_quantity_market_order_allowed: bool
    is_trailing_stop_order_allowed: bool
    is_cancel_replace_allowed: bool
    is_order_amend_allowed: bool
    is_spot_trading_allowed: bool
    is_margin_trading_allowed: bool
    lot_filter: Optional[LotFilter]
    permissions: Optional[List[str]]
    permission_sets: Optional[List[List[str]]]
    default_self_trade_prevention_mode: Optional[str]
    allowed_self_trade_prevention_modes: Optional[List[str]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolInfo":
        lot_filter = next(
            (
                LotFilter.from_dict(f)
                for f in data.get(BinanceResponseKeys.FILTERS, [])
                if f.get(BinanceResponseKeys.FILTER_TYPE) == BinanceResponseValues.LOT_SIZE
            ),
            None
        )


        return cls(
            symbol=data[BinanceResponseKeys.SYMBOL],
            status=data[BinanceResponseKeys.STATUS],
            base_asset=data[BinanceResponseKeys.BASE_ASSET],
            base_asset_precision=data[BinanceResponseKeys.BASE_ASSET_PRECISION],
            quote_asset=data[BinanceResponseKeys.QUOTE_ASSET],
            quote_precision=data[BinanceResponseKeys.QUOTE_PRECISION],
            quote_asset_precision=data[BinanceResponseKeys.QUOTE_ASSET_PRECISION],
            base_commission_precision=data[BinanceResponseKeys.BASE_COMMISSION_PRECISION],
            quote_commission_precision=data[BinanceResponseKeys.QUOTE_COMMISSION_PRECISION],
            supported_order_types=data[BinanceResponseKeys.ORDER_TYPES],
            is_iceberg_order_allowed=data[BinanceResponseKeys.ICEBERG_ALLOWED],
            is_one_cancels_other_allowed=data[BinanceResponseKeys.OCO_ALLOWED],
            is_one_triggers_other_allowed=data[BinanceResponseKeys.OTO_ALLOWED],
            is_quote_quantity_market_order_allowed=data[BinanceResponseKeys.QUOTE_ORDER_QTY_MARKET_ALLOWED],
            is_trailing_stop_order_allowed=data[BinanceResponseKeys.ALLOW_TRAILING_STOP],
            is_cancel_replace_allowed=data[BinanceResponseKeys.CANCEL_REPLACE_ALLOWED],
            is_order_amend_allowed=data[BinanceResponseKeys.AMEND_ALLOWED],
            is_spot_trading_allowed=data[BinanceResponseKeys.IS_SPOT_TRADING_ALLOWED],
            is_margin_trading_allowed=data[BinanceResponseKeys.IS_MARGIN_TRADING_ALLOWED],
            lot_filter=lot_filter,
            permissions=data.get(BinanceResponseKeys.PERMISSIONS),
            permission_sets=data.get(BinanceResponseKeys.PERMISSION_SETS),
            default_self_trade_prevention_mode=data.get(BinanceResponseKeys.DEFAULT_STP_MODE),
            allowed_self_trade_prevention_modes=data.get(BinanceResponseKeys.ALLOWED_STP_MODES),
        )
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def is_symbol_for_trading(self) -> bool:
        return self.status == BinanceResponseValues.TRADING
