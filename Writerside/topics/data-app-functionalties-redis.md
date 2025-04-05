# Redis 

## Core Components

### Redis Connection Setup
- Initializes connection using Django settings:  
  `r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)`  
  Uses database number from `settings.REDIS_DB`

### Core Redis Operations
- `hgetall(name)`  
  + **Purpose**: Get all fields/values from Redis hash  
  + **Inputs**:  
       - `name`: `str` - Redis hash key name (e.g., `'BTC-1h'`)  
  + **Output**: `list` of decoded string values or empty list

- `set(name, value)`  
  + **Purpose**: Set string value in Redis  
  + **Inputs**:  
       - `name`: `str` - Key identifier  
       - `value`: `str` - Value to store  
  + **Output**: Redis operation status

- `get(name)`  
  + **Purpose**: Retrieve string value from Redis  
  + **Inputs**:  
       - `name`: `str` - Key identifier  
  + **Output**: `str` - Decoded value

- `hset(name, key, value)`  
  + **Purpose**: Set field in Redis hash  
  + **Inputs**:  
       - `name`: `str` - Hash key  
       - `key`: `str` - Field name  
       - `value`: `str`/`list` - Value to store (automatically JSON-encoded)  
  + **Output**: Redis operation status

- `hget(name, key)`  
  + **Purpose**: Get JSON-decoded value from Redis hash field  
  + **Inputs**:  
       - `name`: `str` - Hash key  
       - `key`: `str` - Field name  
  + **Output**: `dict`/`list` - Parsed JSON data

- `delete(names)`  
  + **Purpose**: Delete multiple Redis keys  
  + **Inputs**:  
       - `names`: `list` - Array of key names  
  + **Output**: Number of keys deleted

- `keys()`  
  + **Purpose**: Get all Redis keys  
  + **Output**: `list` of byte strings

### Data Management Functions
- `set_history(name, interval)`  
  + **Purpose**: Fetch and store OHLCV data from Binance API  
  + **Inputs**:  
       - `name`: `str` - Trading pair (e.g., `'BTCUSDT'`)  
       - `interval`: `str` - Timeframe from `settings.INTERVALS` (e.g., `'1h'`)  
  + **Output**: Stores parsed data in Redis hash with structure:  
       ```python
       {
           'date': [timestamp1, timestamp2,...],
           'open': [price1, price2,...],
           # other OHLCV fields...
       }
       ```

- `load_history(name, interval, num=0)`  
  + **Purpose**: Retrieve historical data with auto-refresh  
  + **Inputs**:  
       - `name`: `str` - Trading pair  
       - `interval`: `str` - Timeframe specification  
       - `num`: `int` - Recursion guard (default: 0)  
  + **Output**: `dict` of OHLCV lists or empty dict on failure  
  + **Behavior**:  
       - Automatically refreshes stale data (>2 intervals old)  
       - Maximum 1 recursion to prevent loops

### Helper Functions
- `get_history_name(name, interval)`  
  + **Purpose**: Generate standardized Redis key name  
  + **Inputs**:  
       - `name`: `str` - Asset symbol  
       - `interval`: `str` - Timeframe  
  + **Output**: `str` formatted as `'{SYMBOL}-{INTERVAL}'` (e.g., `'BTCUSDT-4h'`)

## Configuration
- `needed_keys`: `list` - Required OHLCV fields for data storage  
  ```python
  ['date', 'open', 'high', 'low', 'close', 'volume']

- `intervals`: Imported from Django settings - Valid timeframe options  

## Maintenance Operations  
- `flushall()`  
  + **Purpose**: Wipe all Redis data  
  + **Output**: Redis operation status  

## Dependencies  
- Uses <include from="third-party-libraries-links.topic" element-id="python-redis"/> for core operations  
- Integrates with [Binance API](finance-app-functionalities-oms.md) for historical data  
- Relies on Django settings for:  
  - Redis database configuration  
  - Valid intervals list  
  - History length limit (`CANDLES_HISTORY_LIMIT`)
