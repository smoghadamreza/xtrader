# Market Watch

## Core Components

### Query Processing Functions
- `query(query_text)`  
   + **Purpose**: Executes filtered market data queries and returns formatted results  
   + **Inputs**:  
        - `query_text`: `str` - Search criteria using symbolic placeholders (e.g., `'(pe) < 20 && (tvol) > 1000000'`)  
   + **Output**: `dict` with two keys:  
        - `'keys'`: Translation dictionary for Persian/English field names  
        - `'result'`: `list` of processed records containing:  
            - Symbol data mapped through `keys` dictionary  
            - Date validation using [Check Class](data-app-functionalities-dates.md#check-class)  
   + **Process Flow**:  
        1. Validates query date using `Check().last_market()`  
        2. Translates symbolic query to database fields  
        3. Executes raw SQL through [](stock-watch-model.md) (as `MarketWatch`)
        4. Converts results using `dict(keys, date)` method  

- `translate(query_text)`  
   + **Purpose**: Converts symbolic query shortcuts to database field names  
   + **Inputs**:  
        - `query_text`: `str` - Original query with placeholder symbols (e.g., `'(pe)'`)  
   + **Output**: `str` - SQL-ready query with actual field names (e.g., `'PricePerEarning'`)  
   + **Mechanism**:  
        - Uses `trans` dictionary for symbol-to-field mapping  
        - Handles logical operators conversion (e.g., `'&&'` → `'AND'`)  

## Misc

### keys Dictionary
`dict` mapping English field names to Persian equivalents:  
```python
{
    'InstrumentName': 'نماد',  # Symbol
    'InstrumentTitle': 'نام',  # Name
    'TotalNumberOfTrades': 'تعداد',  # Transaction Count
    # ... other field mappings ...
}