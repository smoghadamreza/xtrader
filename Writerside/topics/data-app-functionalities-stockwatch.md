# StockWatch

## Core Components

### Database Management

- `createStockWatchTables(num=0)`  
  + **Purpose**: Initializes [](stock-watch-model.md) model records from symbol list  
  + **Inputs**:  
       - `num`: `int` - Start index in symbol list (default: 0)  
  + **Output**: Creates database entries, logs errors to `wrong_symbol_ids`

- `stockWatchInfo(symbol_id, eps=True)`  
  + **Purpose**: Aggregates market data from <include from="third-party-libraries-links.topic" element-id="python-redis"/> and Binance API  
  + **Inputs**:  
       - `symbol_id`: `str` - Trading pair identifier (e.g., `'BTCUSDT'`)  
       - `eps`: `bool` - Earnings data flag (default: `True`, unused in current implementation)  
  + **Output**: `dict` with structure:  
       ```python
       {
           'InstrumentName': str,
           'CompanyName': str,
           'depth': list[dict]  # 10-level order book data
       }
       ```

- `addStockWatchTable(info)`  
  + **Purpose**: Persists collected market data to [](stock-watch-model.md) model  
  + **Inputs**:  
       - `info`: `dict` - Processed market data from `stockWatchInfo()`  
  + **Output**: New database record or error log entry

- `cleanduplicate()`  
  + **Purpose**: Removes duplicate [](stock-watch-model.md) model entries  
  + **Inputs**: None  
  + **Output**: Pruned database table

### Update Operations

#### Stock_Watch Class
- `Stock_Watch.create_tables()`  
  + **Purpose**: Entry point for table initialization (static method)  
  + **Output**: Calls `createStockWatchTables()`

- `Stock_Watch.update(self, num=0)`  
  + **Purpose**: Updates existing [](stock-watch-model.md) model records  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
       - `num`: `int` - Start index for updates (default: 0)  
  + **Output**: Modified database records, error logging

- `update_stock_watch(num=0)`  
  + **Purpose**: Batch update processor for market data  
  + **Inputs**:  
       - `num`: `int` - Start index in records (default: 0)  
  + **Output**: Calls `updateStockWatchTable()` for each valid record

- `updateStockWatchTable(model, data)`  
  + **Purpose**: Applies updated market data to existing [](stock-watch-model.md) model  
  + **Inputs**:  
       - `model`: [](stock-watch-model.md) model instance  
       - `data`: `dict` - New market data from `stockWatchInfo()`  
  + **Output**: Updated database record

## Data Flow
1. Initializes through `Stock_Watch.create_tables()`  
2. Uses [Binance API](finance-app-functionalities-oms.md) via `oms.Binance.get_depth()`  
3. Stores raw data in <include from="third-party-libraries-links.topic" element-id="python-redis"/>  
4. Transforms data with `stockWatchInfo()`  
5. Persists to database via Django ORM

## Error Handling
- Failed operations logged in `wrong_symbol_ids` list  
- Duplicate protection through `cleanduplicate()`  
- Index-based restart capability via `num` parameter

## Dependencies
- Requires [](stock-watch-model.md) model model definition  
- Integrates with `oms.Binance` for real-time market data  
- Relies on <include from="third-party-libraries-links.topic" element-id="python-redis"/> for temporary storage
