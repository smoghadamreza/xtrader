# Indicators 

## Core Components

### Technical Indicator Core
#### Indicator Class
- `Indicator.__init__(self, name=None, tail=None, interval=None)`  
   + **Purpose**: Initializes indicator calculator with historical data  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
        - `name`: `str` - Financial instrument symbol (e.g., `'BTC/USDT'`)  
        - `tail`: `dict` - Real-time price updates (e.g., `{'price': {'open': 50000}}`)  
        - `interval`: `str` - Mandatory timeframe specification (e.g., `'1h'`, `'4h'`)  
   + **Output**:  
        - Initializes Indicator instance with:  
            - `self.df`: Empty <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> (if no name provided) or loaded OHLCV data  
            - `self.inputs`: `dict` of <include from="third-party-libraries-links.topic" element-id="numpy-array"/>s for <include from="third-party-libraries-links.topic" element-id="ta-lib"/> calculations  
            - `self.interval`: Set timeframe for data loading  
        - Returns `None`

- `Indicator.set_symbol(self, name, tail=None)`  
   + **Purpose**: Loads historical data from <include from="third-party-libraries-links.topic" element-id="python-redis"/> database  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
        - `name`: `str` - Symbol identifier (e.g., `'EUR/USD'`)  
        - `tail`: `dict` - Partial current candle data to update 
   + **Output**:  
        - Updates instance with:  
            - `self.df`: OHLCV DataFrame with updated tail prices (if provided)  
            - `self.inputs`: Converted <include from="third-party-libraries-links.topic" element-id="numpy-array"/>s of price data  
            - `self.SymbolId`: Set symbol identifier 
        - Returns `None`

- `Indicator.load_db(self, tail=None)`  
   + **Purpose**: Retrieves and formats historical data from <include from="third-party-libraries-links.topic" element-id="python-redis"/>  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
        - `tail`: `dict` - Optional price updates for most recent period  
   + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with OHLCV data and time index  

- `Indicator.ichimoku(self, *args, **kwargs)`  
   + **Purpose**: Calculates Ichimoku Cloud components  
   + **Inputs** (via kwargs):  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
        - `conversionLineperiod`: `float` - Tenkan-sen period (typically 9)  
        - `BaseLineperiod`: `int` - Kijun-sen period (typically 26)  
        - `LagingB`: `float` - Senkou Span B period (typically 52)  
   + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with 5 columns:  
        - `'Tenkan-sen'`, `'Kijun-sen'`, `'Senkou Span A'` `'Senkou Span B'`, `'Chikou Span'`  


- `Indicator.indicator_calculator(self, function_name, symbol_name=None, tail=None, *args, **kwargs)`  
   + **Purpose**: Main calculation engine for all indicators  
   + **Inputs**:
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>
        - `function_name`: `str` - Indicator name (e.g., `'RSI'`, `'ICHIMOKU'`)  
        - `symbol_name`: `str` - Optional symbol override  
        - `tail`: `dict` - Real-time price updates  
        - `*args/**kwargs`: Indicator-specific parameters  
   + **Output**: Returns single or multi-column <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> depending on indicator type

### API Management

- `get_parameter(function_name)`  
   + **Purpose**: Returns parameter metadata for given <include from="third-party-libraries-links.topic" element-id="ta-lib"/> indicator  
   + **Inputs**:  
        - `function_name`: `str` - <include from="third-party-libraries-links.topic" element-id="ta-lib"/> function name (e.g., `'RSI'`)  
   + **Output**: `dict` of parameter names and default values  

- `get_group_api()`  
   + **Purpose**: Organizes indicators into logical groups  
   + **Output**: `dict` with 3-level structure:  
        ```
        Group -> Indicator Name -> {params, settings, outputs}
        ```

- `get_ti_api()`  
   + **Purpose**: Generates flat list of all available indicators  
   + **Output**: `dict` with indicator names as keys and metadata as values  

### Data Utilities
- `add_time(df)`  
   + **Purpose**: Adds explicit timestamp column to DataFrame  
   + **Inputs**:  
        - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Time-indexed data  
   + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with `'time'` as first column  

- `to_json(df)`  
   + **Purpose**: Serializes <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/>  with timestamps  
   + **Inputs**:  
        - `df`: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> - Data to convert  
   + **Output**: `str`  <include from="third-party-libraries-links.topic" element-id="python-json"/> string with array format  

- `read_json(json)`  
   + **Purpose**: Reconstructs time-indexed <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> 
  from <include from="third-party-libraries-links.topic" element-id="python-json"/>  
   + **Inputs**:  
        - `json`: `str` - <include from="third-party-libraries-links.topic" element-id="python-json"/> string from `to_json()`  
   + **Output**: <include from="third-party-libraries-links.topic" element-id="pandas-dataframe"/> with original structure 

## Misc

### Rename_group_name_dic
`dict` mapping <include from="third-party-libraries-links.topic" element-id="ta-lib"/> groups to custom categories:  
```python
Rename_group_name_dic = {
    'fields': 'Historical Data',
    'Volume Indicators': 'Volume Indicators',
    # ... other mappings ...
    'Math Operators': None  # Excluded groups
}
```

### Bad_indicators
`list` of excluded <include from="third-party-libraries-links.topic" element-id="ta-lib"/> functions

## DataFlow

<include from="architecture-diagrams.topic" element-id="finance-app-data-flow-diagram"></include>
