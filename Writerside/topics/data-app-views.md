# Views

<include from="repeatable-texts.topic" element-id="django-views">
</include>

## Functions

### `history`

This function retrieves historical market data for all symbols from Redis storage.

#### Behavior {id=behavior_1}
- Fetches all symbol keys from Redis database
- For each symbol, collects date, close, open, high, low, and volume fields when available
- Returns JSON array of symbol dictionaries with available data
- Silently handles missing fields without failing
- Makes multiple Redis queries (one per field per symbol)

### `stockwatch`

This function retrieves watch information for a specific stock symbol.

#### Input Parameters {id=input_param_2}
- request: Standard Django HttpRequest object
- SymbolId: The identifier of the stock symbol to look up

#### Behavior {id=behavior_2}
- Takes a stock symbol ID as parameter
- Calls stockwatchModel.stockWatchInfo() with the SymbolId and EPS data flag
- Returns the raw stock watch information as JSON response
- Uses direct JSON serialization of model data

### `symbol_search`

This function performs a search for financial symbols matching the query string.

#### Input Parameters {id=input_param_3}
- request: Standard Django HttpRequest
- query: Search string to match against symbol names

#### Behavior {id=behavior_3}
- Gets all symbol data from Redis hash "exchangeInfo"
- Filters symbols containing query string (case-insensitive)
- Constructs response with symbol details including quote/base assets
- Returns UTF-8 encoded JSON response limited to 10 matches

### `get_data`

This function retrieves historical market data for a specific symbol and time interval.

#### Input Parameters {id=input_param_4}
- request: Standard Django HttpRequest
- symbol_id: Financial symbol identifier
- interval: Time interval for historical data

#### Behavior {id=behavior_4}
- Retrieves historical data from Redis using symbol and interval
- Converts data to pandas DataFrame with date index
- Gets symbol metadata from Redis "exchangeInfo" hash
- Returns JSON with symbol information and historical data

### `get_symbols`

This function retrieves all available symbol identifiers from the database.

#### Input Parameters {id=input_param_5}
- request: Standard Django HttpRequest

#### Behavior {id=behavior_5}
- Queries all records from the Symbol model
- Extracts SymbolId field from each record
- Returns array of symbol IDs in JSON format
- Uses Django's ORM for database access

### `get_all_symbols`

This function retrieves all available trading symbols from Redis.

#### Input Parameters {id=input_param_6}
- request: Standard Django HttpRequest object

#### Behavior {id=behavior_6}
- Retrieves all symbol data from Redis hash "exchangeInfo"
- Creates simplified symbol objects containing only title field
- Returns JSON response with array of all symbols

### `get_intervals`

This function returns available trading intervals and user's preferred interval.

#### Input Parameters {id=input_param_7}
- request: Standard Django HttpRequest object

#### Behavior {id=behavior_7}
- For authenticated users:
  - Checks for user's strategy preference
  - Returns default '4h' interval if no strategy exists
- For anonymous users:
  - Returns only default intervals
- Combines system intervals with user's preferred interval
