# Scan

## Core Components

### Scanning Orchestration
- `screener(interval)`  
  + **Purpose**: Main entry point for market scanning across all strategies  
  + **Inputs**:  
       - `interval`: `str` - Analysis timeframe (e.g., `'1h'`, `'4h'`)  
  + **Behavior**:  
       1. Iterates through all strategy traders  
       2. Validates [](accounts-app-models.md) and subscription status  
       3. Initiates parallel scanning via `scan_thread`  
       4. Manages [](payment-model.md) transactions for scan costs  
  + **Output**:
    - Returns `None`

- `scan_thread(username, strategy_name, strategy_id, telegram_id, interval, watchlist_id, watchlist_name)`  
  + **Purpose**: Thread worker for strategy-specific scanning  
  + **Inputs**:  
       - `username`: `str` - Trader identifier  
       - `strategy_id`: `int` - [](strategy-model.md) ID  
       - `telegram_id`: `int` - Notification target ID  
       - `watchlist_id`: `int` - Custom watchlist identifier  
       - Other parameters: Strategy metadata and timeframe  
  + **Output**: Sends formatted Telegram message via [](finance-app-functionalities-notification.md)

### Market Analysis Engine
- `scan_market(user_name, strategy_id, former=True)`  
  + **Purpose**: Executes technical analysis for given strategy  
  + **Inputs**:  
       - `user_name`: `str` - Trader username  
       - `strategy_id`: `int` - Strategy database ID  
       - `former`: `bool` - Historical comparison flag (default: `True`)  
  + **Output**: `dict` with:  
       ```python
       {
           'buy': list[dict],  # Symbols with buy signals
           'sell': list[dict]  # Symbols with sell signals
       }
       ```

## Helper Functions

### Strategy Configuration
- `find_strategy_filters(user_name, strategy_id)`  
  + **Purpose**: Retrieves strategy parameters from database  
  + **Inputs**:  
       - `user_name`: `str` - Trader identifier  
       - `strategy_id`: `int` - Strategy record ID  
  + **Output**: Tuple of `(filters, interval, symbol_ids)`

### Signal Calculation
- `calculate_filter_result(strategy_filter, interval)`  
  + **Purpose**: Applies technical analysis filter to symbol  
  + **Inputs**:  
       - `strategy_filter`: `dict` - Filter configuration  
       - `interval`: `str` - Timeframe specification  
  + **Output**: `dict` with:  
       ```python
       {
           'type': 'first'|'second',  # Signal category
           'result': list  # Raw analysis results
       }
       ```

### Result Processing
- `check_first_kind(results)`  
  + **Purpose**: Aggregates primary signal type results  
  + **Inputs**:  
       - `results`: `dict` - Multiple filter outputs  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="numpy-array"/> of consolidated signals  

- `final_check(final_dict)`  
  + **Purpose**: Generates final trading signals from processed data  
  + **Inputs**:  
       - `final_dict`: `dict` - Combined first/second-type results  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="numpy-array"/> of buy/sell recommendations  

## Notification Formatting
All messages include:  
- Strategy name and timeframe  
- Watchlist details  
- Direct trading view links  
- Subscription upgrade prompts when applicable  

## Concurrency Handling
- Uses <include from="repeatable-texts.topic" element-id="python-threading"/> for parallel market scans  
- Maintains active DB connections through `connections.all()` management  

## Dependencies
- Integrates with [](finance-app-functionalities-data-handling.md) for technical analysis  
- Requires [](finance-app-functionalities-strategy.md) for package limits  
- Utilizes [](finance-app-functionalities-notification.md) for Telegram delivery  
