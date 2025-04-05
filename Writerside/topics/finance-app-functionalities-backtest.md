# Backtest Engine 

## Core Components

### Signal Generation Functions
- `cross(shorter, longer)`  
  + **Purpose**: Detects crossover points between two indicators  
  + **Inputs**:  
       - `shorter`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Fast moving indicator values  
       - `longer`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Slow moving indicator values  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with `1` (upcross), `-1` (downcross), `0` (no cross)

- `cross_buy(shorter, longer)`  
  + **Purpose**: Detects upward crossover points for buy signals  
  + **Inputs**:  
       - `shorter`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Fast moving indicator (e.g., 50-day SMA)  
       - `longer`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Slow moving indicator (e.g., 200-day SMA)  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with:  
       - `1` when shorter crosses above longer  
       - `0` otherwise  
  + **Example**:  
       ```python
       # Detects when 50EMA crosses above 200EMA
       buy_signals = cross_buy(ema_50, ema_200)
       ```

- `cross_sell(shorter, longer)`  
  + **Purpose**: Specialized cross detection for long/short entry signals  
  + **Inputs**: 
     - `shorter`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Fast moving indicator (e.g., 50-day SMA)  
     - `longer`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Slow moving indicator (e.g., 200-day SMA)  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with `1` at valid crosses, `0` elsewhere

### Data Processing Utilities
- `merge(buy_df, sell_df)`  
  + **Purpose**: Combines buy/sell signals into unified series  
  + **Inputs**:  
       - `buy_df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Buy signals (`1`)  
       - `sell_df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Sell signals (`1`)  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with merged `1`/`-1`/`0` values

- `set_valid_time(df, time=0)`  
  + **Purpose**: Extends signal validity period  
  + **Inputs**:  
       - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Raw signals  
       - `time`: `int` - Number of periods to maintain signal (default=0)  
  + **Output**: Smoothed <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/>

- `change_df(df)`  
  + **Purpose**: Standardizes DataFrame column names  
  + **Inputs**:  
       - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with any column names  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with numeric columns ('0','1',...)

- `shifter(df, shift_time)`  
  + **Purpose**: Creates lagged version of input data  
  + **Inputs**:  
       - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/>  
       - `shift_time`: `int` - Periods to offset  
  + **Output**: Lagged <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/>

### Trend Analysis
- `monotono(indicator, days=2, angel=90)`  
  + **Purpose**: Identifies sustained upward/downward trends  
  + **Inputs**:  
       - `indicator`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Input values  
       - `days`: `int` - Minimum trend duration (default=2)  
       - `angel`: `int` - Slope threshold (unused in current implementation)  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with `1` (up), `-1` (down), `0`

- `more_than(main, minor, days=0)`  
  + **Purpose**: Threshold comparison between two indicators  
  + **Inputs**:  
       - `main`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Primary indicator  
       - `minor`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Comparison baseline  
       - `days`: `int` - Minimum consecutive periods (default=0)  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with `1` where main > minor for `days` periods

- `ascending(diff, days, result, value=100)`  
- `descending(diff, days, result)`  
  + **Purpose**: Trend confirmation helpers for `monotono()`  
  + **Inputs**:  
       - `diff`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Price difference series  
       - `days`: `int` - Minimum trend duration  
       - `result`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Result container  
       - `value`: `int` - Signal strength (ascending only)  
  + **Output**: Modified `result` with trend flags

### Special Signal Handlers
- `special(indicators, name)`  
  + **Purpose**: Processes complex indicators (MACD/Ichimoku)  
  + **Inputs**:  
       - `indicators`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Raw indicator values  
       - `name`: `str` - Indicator type ('MACD' or 'ichimoku')  
  + **Output**: Processed <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with trading signals

- `give_macd_result(indicators)`  
  + **Purpose**: Generates MACD-specific trading signals  
  + **Inputs**:  
       - `indicators`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with 'macd' and 'macdsignal' columns  
  + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with convergence/divergence signals (`1`/-`1`/`0`)

### Backtest Engine
#### BackTest Class
- `BackTest.__init__(self, price, trades, config)`  
  + **Purpose**: Initializes backtest environment  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `price`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Historical prices  
       - `trades`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Trading signals  
       - `config`: `dict` - Risk parameters:  
           ```python
           {
               'stop loss': 2.0,  # Percentage value
               'take profit': 3.0,  # Percentage value
               'initial deposit': 10000  # Starting capital
           }
           ```

- `BackTest.back_test(self)`  
  + **Purpose**: Executes full backtest simulation  
  + **Input**:
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
  + **Output**: `dict` containing:  
       - `result`: Detailed trade-by-trade records  
       - `summery`: Aggregated performance metrics  

- `BackTest.order(self, details, kind)`  
  + **Purpose**: Records trade execution details  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `details`: `dict` - Trade parameters (price, date, etc.)  
       - `kind`: `str` - Trade type ('buy'/'sell'/'nothing')  
  + **Output**: Updates `self.result` dictionary with trade records

- `BackTest.change_other_things(self, kind, i)`  
  + **Purpose**: Manages position state transitions  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `kind`: `str` - Action type ('buy'/'sell')  
       - `i`: `int` - Index position in price data  
  + **Output**: Updates position tracking variables (`position`, `days_in_trade`, etc.)

- `BackTest.sell(self, i, sell_type)`  
  + **Purpose**: Calculates sell order metrics  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `i`: `int` - Data index position  
       - `sell_type`: `str` - Reason for sell ('stoploss'/'takeprofit'/'sell')  
  + **Output**: `dict` with:  
       ```python
       {
           "date": "2023-01-05", 
           "action": "sell",
           "price": "46723.50",
           "return": "2.34",  # Percentage return
           "candles in trade": 5,  # Holding period
           "capital": 10234.00  # Updated balance
       }
       ```
    
- `BackTest.buy(self, i)`  
  + **Purpose**: Processes buy order initialization  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `i`: `int` - Entry position index  
  + **Output**: `dict` with:  
       ```python
       {
           "action": "buy",
           "date": "2023-01-01",
           "price": "45678.90",
           "waiting candles": 3  # Period since last trade
       }
       ```

- `BackTest.check_last_trade(self)`  
  + **Purpose**: Handles unresolved positions at backtest end  
  + **Input**:
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
  + **Output**: Forces closure of open positions, marks as 'Not Sold Yet'

- `BackTest.call_order_and_change(self, details, order_type, i)`  
  + **Purpose**: Unified trade execution handler  
  + **Inputs**:  
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
       - `details`: `dict` - Trade parameters  
       - `order_type`: `str` - Trade direction  
       - `i`: `int` - Data index  
  + **Output**: Updates order records and position state

- `BackTest.backtest_result(self)`  
  + **Purpose**: Main backtest simulation loop  
   + **Input**:
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
   + **Output**: Populates `self.result` with complete trade history

- `BackTest.summery(self)`  
  + **Purpose**: Generates aggregated performance metrics  
   + **Input**:
       - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
  + **Output**: `dict` with:  
       ```python
       {
           "average": {
               "candles in trade": 5.2,
               "waiting candles": 3.1,
               "profits": 2.8
           },
           "std": {  # Standard deviations
               "candles in trade": 1.7,
               "waiting candles": 0.9,
               "profits": 1.2
           }
       }
       ```
    
## Signal Filtering

- `buy_output_for_display(df, signaldf)`  
  + **Purpose**: Extracts valid buy signals for visualization  
  + **Inputs**:  
       - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Raw price/indicator data  
       - `signaldf`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Trading signals (`1`=buy, `-1`=sell, `0`=neutral)  
  + **Output**: Filtered <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> containing only rows with buy signals

- `sell_output_for_display(df, signaldf)`  
  + **Purpose**: Filters valid buy/sell signals from raw data  
  + **Inputs**:  
       - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Price/indicator values  
       - `signaldf`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Trading signals  
  + **Output**: Filtered <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> showing only signal points

## Misc Functions
- `testresult(price, trades, config)`  
  + **Purpose**: Alternative backtest implementation with commission handling  
  + **Inputs**: Same as `BackTest` class plus:  
       - `selling_commision`: `float` - Transaction cost for sells (default=0.001)  
       - `buying_commision`: `float` - Transaction cost for buys (default=0.001)  
  + **Output**: Enhanced `dict` with financial metrics

## Key Data Structures
All functions operate on <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with:
- Index: Datetime index  
- Columns: Single column `0` containing numerical values  
- Example row: `2023-01-01 00:00:00 → 1` (buy signal)

## Performance Metrics
Successful trades include:
- Entry/exit prices
- Holding period duration
- Return percentage
- Commission costs
- Updated capital balance

## DataFlow
<include from="architecture-diagrams.topic" element-id="finance-app-data-flow-diagram"/>
