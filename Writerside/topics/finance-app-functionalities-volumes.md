# Volumes

## Core Components

### Backtest Execution
- `run_test(data)`  
  + **Purpose**: Initializes backtest using historical data index  
  + **Inputs**:  
       - `data`: `dict` containing:  
           - `symbol_id`: `str` - Market identifier (e.g., `'IRO1KAVR0001'`)  
           - `index`: `int` - Starting point in historical data  
  + **Output**: Returns `buy_volume_decrease()` results with adjusted index  

### Trading Strategy Core
- `buy_volume_decrease(index=0, initial=10000000, symbol_id='IRO1KAVR0001', takeprofit=0.3, stoploss=0.1)`  
  + **Purpose**: Simulates volume-averaged mean reversion strategy  
  + **Inputs**:  
       - `index`: `int` - Starting index in historical data (default: 0)  
       - `initial`: `float` - Initial capital (default: 10,000,000)  
       - `symbol_id`: `str` - Market identifier (default: `'IRO1KAVR0001'`)  
       - `takeprofit`: `float` - Profit target ratio (default: 0.3)  
       - `stoploss`: `float` - Loss threshold ratio (default: 0.1)  
  + **Output**: `dict` with:  
       ```python
       {
           'history': list[dict],  # Trade records
           'status': 'worked'|'running',  # Strategy outcome
           'finishdate': int,  # Unix timestamp (if exited),
           'dates': list[int]  # Buy timestamps
       }
       ```

### Position Sizing
- `calc_vol(history, price, takeprofit=0.1)`  
  + **Purpose**: Calculates position size based on cumulative loss  
  + **Inputs**:  
       - `history`: `list[dict]` - Previous trade records  
       - `price`: `float` - Current asset price  
       - `takeprofit`: `float` - Target profit ratio (default: 0.1)  
  + **Output**: `int` - Calculated position size  

### Multi-Symbol Testing
- `test()`  
  + **Purpose**: Runs strategy simulation across multiple symbols  
  + **Output**: `dict` mapping symbols to test results:  
       ```python
       {
           'SYMBOL': [
               {'i': int, 'margin': float, 'action': str},  # Negative P&L instances
               # ... additional results
           ]
       }
       ```

## Key Metrics
- **Takeprofit Activation**: Triggers at `(1 + takeprofit) * entry_price`  
- **Stoploss Calculation**: Converts input to `1 - stoploss` for downside threshold  
- **Margin Management**: Tracks available capital after each position  

## Data Flow
1. Historical data loaded via <include from="third-party-libraries-links.topic" element-id="python-redis"/> `load_history` 
2. Trade decisions made using `close` and `high` price series  
3. Position sizing adjusted dynamically through `calc_vol()`  

## Simulation Features
- Maintains complete trade history with timestamps  
- Detects margin calls when available funds < 0  
- Supports multiple asset testing through `test()`  

## Dependencies
- Requires <include from="third-party-libraries-links.topic" element-id="python-redis"/> for price data access  
