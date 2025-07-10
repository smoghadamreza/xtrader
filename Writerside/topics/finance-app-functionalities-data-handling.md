# Data Handling

## Core Result Generation Functions

### Comparative Analysis
#### give_result_more()
- `give_result_more(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Compares two indicators (main vs minor) using threshold logic  
   + **Inputs**:  
        - `data`: `dict` - Configuration containing:  
            ```python
                {
                'symbol_id': 'BTC/USDT',  # Market symbol
                'valid': 3,  # Validation period length
                'indicators': {
                    'main': {'name': 'RSI', 'params': {'timeperiod':14}, ...},
                    'minor': {'name': 'SMA', 'params': {'timeperiod':30}, ...}
                }
            }
            ```
        - `mt`: `Indicator` - Optional pre-initialized indicator calculator  
        - `get_json`: `bool` - Return format toggle (True=JSON, False=dict)  
        - `interval`: `str` - Timeframe (e.g., '4h')  
   + **Output**:  
        - Returns `str` <include from="third-party-libraries-links.topic" element-id="python-json"/> or `dict` with:  
            ```python
            {
                'main': {output_data},  # Main indicator values
                'minor': {output_data},  # Secondary indicator values
                'result': [[timestamp, 1], ...],  # 1/0 signals
                'type': 'second'  # Result classification
            }
            ```

### Special Signal Analysis
#### give_result_special()
- `give_result_special(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Generates signals for pattern-based indicators  
   + **Inputs**:  
        - `data`: `dict` - Must contain 'special' indicator config  
        - Other parameters match `give_result_more()`  
   + **Output**:  
        - Returns JSON/dict with:  
            ```python
            {
                'special': {output_data},  # Pattern detection values
                'result': [[timestamp, signal_strength], ...],
                'type': 'first'  # Direct signal classification
            }
            ```

### Trend Analysis
#### give_result_ascending()
- `give_result_ascending(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Identifies sustained price trends  
   + **Inputs**:  
        - `data`: `dict` - Requires 'days' parameter for trend duration  
        - Other parameters match base signature  
   + **Output**:  
        ```python
        {
            'ascending': {output_data},  # Trend indicator values
            'result': [[timestamp, trend_strength], ...],
            'type': 'first'
        }
        ```

### Visual Drawing Tools
#### give_result_draw()
- `give_result_draw(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Returns raw indicator values for chart display  
   + **Inputs**:  
        - `data`: `dict` - Focused on 'draw' indicator configuration  
   + **Output**:  
        ```python
        {
            'draw': {output_data},  # Full historical values
            'type': 'default'  # Raw data classification
        }
        ```

### Candlestick Pattern Detection
#### give_result_candlestick()
- `give_result_candlestick(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Detects predefined candlestick patterns  
   + **Inputs**:  
        - Requires 'candlestick' indicator config in data  
   + **Output**:  
        ```python
        {
            'candlestick': {pattern_metrics},
            'result': [[timestamp, pattern_code], ...],  # -1,0,1 signals
            'type': 'first'
        }
        ```

### Crossover Analysis
#### give_result_cross()
- `give_result_cross(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Detects crosses between two indicators  
   + **Inputs**:  
        - `data`: `dict` - Contains 'shorter' and 'longer' indicator configs  
   + **Output**:  
        ```python
        {
            'shorter': {fast_indicator},
            'longer': {slow_indicator},
            'result': [[timestamp, cross_direction], ...],  # 1=upcross, -1=downcross
            'type': 'first'
        }
        ```

### Advanced Trading Signals
#### give_result_advance_cross()
- `give_result_advance_cross(data, mt=None, get_json=True, interval=None)`  
   + **Purpose**: Generates complex entry/exit signals using 4 indicators  
   + **Inputs**:  
        - `data`: `dict` - Contains separate configs for:  
            ```python
            'buying shorter', 'buying longer', 
            'selling shorter', 'selling longer'
            ```
   + **Output**:  
        ```python
        {
            'buying shorter': {entry_fast_indicator},
            'buying longer': {entry_slow_indicator},
            'selling shorter': {exit_fast_indicator},
            'selling longer': {exit_slow_indicator},
            'result': [[timestamp, net_signal], ...],  # Combined signals
            'type': 'first'
        }
        ```

## Backtesting Utilities

### give_result_backtest()
- `give_result_backtest(name, res, config, interval=None)`  
   + **Purpose**: Executes backtest with given signals and strategy rules  
   + **Inputs**:  
        - `name`: `str` - Symbol ID  
        - `res`: `list` - Signal data from other functions  
        - `config`: `dict` - Risk parameters:  
            ```python
            {
                'stop loss': {'value':2, 'apply':'ATR'}, 
                'take profit': {'value':3, 'apply':'Volatility'}
            }
            ```
   + **Output**: <include from="third-party-libraries-links.topic" element-id="python-json"/> with backtest metrics  

### give_update_indicators()
- `give_update_indicators(data)`  
   + **Purpose**: Real-time indicator updates for streaming systems  
   + **Inputs**:  
        - `data`: `dict` - Contains latest price and indicator params  
   + **Output**: `str` JSON with latest indicator values  

## Helper Functions

### add_apply_to()
- `add_apply_to(indicator_dic, indicator_name, data)`  
   + **Purpose**: Modifies indicator calculation source (price/other)  
   + **Inputs**:  
        - `indicator_dic`: `dict` - Base indicator config  
        - `indicator_name`: `str` - Target indicator type  
        - `data`: `dict` - Full request configuration  
   + **Output**: Modified `indicator_dic` with 'price' field if needed  

## Data Flow

<include from="architecture-diagrams.topic" element-id="finance-app-data-flow-diagram"/>