from finance.exchange.data import SymbolInfo
from dataclasses import dataclass, asdict

@dataclass
class SymbolSearchResult:
    symbol_id: str
    kind: str
    category: str
    symbol_name: str
    name: str
    description: str
    title: str

    @classmethod
    def load_from_symbol_info(cls, info: SymbolInfo) -> "SymbolSearchResult":
        return cls(
            symbol_id = info.symbol,
            symbol_name = info.symbol,
            kind = info.quote_asset,
            category = info.base_asset,
            name = ", ".join(info.permissions or []),
            description="self.CompanyName",  # placeholder
            title="title",  # placeholder
        )
    
    def to_dict(self) -> dict:
        return asdict(self)
