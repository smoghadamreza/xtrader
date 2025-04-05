# Binance Integration Documentation (OMS)

## Core Components

### Binance API Client
#### Binance Class (Static Methods)

- `Binance.get_candles(params)`  
  + **Purpose**: Retrieve OHLCV data from Binance API  
  + **Inputs**:  
       - `params`: `dict` - Contains:  
           - `symbol`: `str` (e.g., `'BTCUSDT'`)  
           - `interval`: `str` (e.g., `'1h'`)  
           - `limit`: `int` - Candle count  
  + **Output**: `list` of candle arrays `[open_time, open, high, low, close, ...]`

- `Binance.get_depth(symbol_id, limit=10)`  
  + **Purpose**: Get order book data with Redis caching  
  + **Inputs**:  
       - `symbol_id`: `str` - Trading pair  
       - `limit`: `int` - Price levels (default: 10)  
  + **Output**: `dict` with `bids`, `asks`, and `lastUpdateTime`

- `Binance.set_symbols()`  
  + **Purpose**: Cache symbol metadata in <include from="third-party-libraries-links.topic" element-id="python-redis"/>  
  + **Output**: Stores `dict` of symbol info under `exchangeInfo` key

- `Binance.lot_filter(symbol, qty)`  
  + **Purpose**: Apply Binance LOT_SIZE trading rules  
  + **Inputs**:  
       - `symbol`: `str` - Trading pair  
       - `qty`: `float` - Raw quantity  
  + **Output**: `str` - Rounded quantity meeting exchange filters

- `Binance.send_order(ex, params)`  
  + **Purpose**: Submit order to Binance API  
  + **Inputs**:  
       - `ex`: [](exchange-model.md) model instance  
       - `params`: `dict` - Order parameters:  
           - `symbol`, `side`, `type`, `quantity`, `price`  
  + **Output**: `dict` with:  
       - `error`: `bool` - Success status  
       - `msg`: `str` - Error description if applicable

### Order Management

- `Binance.cancel_order(ex, symbol, order_id)`  
  + **Purpose**: Cancel active order  
  + **Inputs**:  
       - `ex`: [](exchange-model.md) model  
       - `symbol`: `str` - Trading pair  
       - `order_id`: `int` - Order identifier  
  + **Output**: Binance API response `dict`

- `Binance.cancel_all_orders(ex, symbol)`  
  + **Purpose**: Cancel all open orders for symbol  
  + **Inputs**:  
       - `ex`: [](exchange-model.md) model  
       - `symbol`: `str` - Trading pair  
  + **Output**: API response `dict`

### Portfolio Operations

- `Binance.get_portfolio(ex)`  
  + **Purpose**: Retrieve account balances  
  + **Inputs**:  
       - `ex`: [](exchange-model.md) model  
  + **Output**: `list` of asset `dicts` with `symbol`, `free`, `locked`

- `Binance.get_historical_trades(symbol, public, private)`  
  + **Purpose**: Fetch full trade history  
  + **Inputs**:  
       - `symbol`: `str` - Trading pair  
       - `public`: `str` - API key  
       - `private`: `str` - Secret key  
  + **Output**: `list` of trade `dicts` with `id`, `price`, `qty`, etc.

### Price Utilities

- `Binance.get_last_price(symbol)`  
  + **Purpose**: Get cached price with 30-second TTL  
  + **Inputs**:  
       - `symbol`: `str` - Trading pair  
  + **Output**: `float` - Last traded price from Redis or API

## Copy Trading System
#### OMSManager Class

- `OMSManager.get_exchange(request, trader=None)`  
  + **Purpose**: Retrieve trader's exchange connection  
  + **Inputs**:  
       - `request`: <include from="repeatable-texts.topic" element-id="http-request"/>  
       - `trader`: `User` - Optional override  
  + **Output**: Tuple of (`Exchange` instance, `Binance` class)

- `OMSManager.copytrade(trader, new_order, followers=[])`  
  + **Purpose**: Replicate trades to follower accounts  
  + **Inputs**:  
       - `trader`: `User` - Strategy source  
       - `new_order`: `dict` - Order template  
       - `followers`: `list` - [](social-app-models.md) instances  
  + **Behavior**: Spawns threads for parallel order execution

## Security Implementation

- `Binance.sign(params, private)`  
  + **Purpose**: Generate HMAC-SHA256 API signature  
  + **Inputs**:  
       - `params`: `dict` - Request parameters  
       - `private`: `str` - API secret key  
  + **Output**: Signed query string for API authentication

## Historical Data

- `Binance.get_historical_nav(public, private)`  
  + **Purpose**: Calculate Net Asset Value timeline  
  + **Inputs**:  
       - `public`: `str` - API key  
       - `private`: `str` - Secret key  
  + **Output**: `list` of NAV snapshots with timestamps

## Dependencies

- Uses <include from="third-party-libraries-links.topic" element-id="python-requests"/> for API communication  
- Integrates with [](exchange-model.md) model model  
- Requires Redis for:  
  - Order book caching (`Depth` key)  
  - Symbol metadata storage (`exchangeInfo` key)  
  - Price caching (`LASTPRICE` key)
