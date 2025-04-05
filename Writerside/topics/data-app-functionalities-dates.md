# Dates

## Core Components

### Date/Time Utilities

- `to_timestamp(date, mode)`  
   + **Purpose**: Converts date string to millisecond timestamp based on calendar system  
   + **Inputs**:  
        - `date`: `str` - Date string in format:  
            - `'YYYYMMDDHHmmss'` for `'mabna'` mode (e.g., `'20210515124530'`)  
            - `'YYYY-MM-DD HH:mm:ss'` for `'farabi'` mode (e.g., `'2021-05-15 12:45:30'`)  
        - `mode`: `str` - Calendar system: `'farabi'` (Gregorian) or `'mabna'` (Persian)  
   + **Output**: `int` - Unix timestamp in milliseconds  

- `fix_date_mabna(date)`  
   + **Purpose**: Converts Persian calendar date to UTC-adjusted Gregorian timestamp  
   + **Inputs**:  
        - `date`: `str` - 14-character string in `'YYYYMMDDHHmmss'` format  
   + **Output**: `int` - UTC timestamp (ms) with timezone conversion (UTC+3:30 → UTC)  

- `fix_date_farabi(date)`  
   + **Purpose**: Converts Gregorian date string to UTC-adjusted timestamp  
   + **Inputs**:  
        - `date`: `str` - Date in `'YYYY-MM-DD HH:mm:ss'` format  
   + **Output**: `int` - UTC timestamp (ms) with timezone conversion (UTC+3:30 → UTC)  

- `to_str(date)`  
   + **Purpose**: Formats date object to `'YYYY-MM-DD'` string  
   + **Inputs**:  
        - `date`: `datetime` - Python datetime object  
   + **Output**: `str` - Truncated date string (e.g., `'2023-07-20'`)  

### Market Status Checker
#### Check Class
- `Check.__init__(self)`  
   + **Purpose**: Initializes market checker with current datetime  
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Outputs**
     - Returns `None`

- `Check.day(self)`  
   + **Purpose**: Checks if current day is market weekday  
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Output**: `bool` - `True` if not Thursday/Friday  

- `Check.time(self)`  
   + **Purpose**: Verifies if within market hours (8:30-12:30 UTC+3:30)  
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Output**: `dict` with:  
      - `market_time`: `bool` - Trading window status  
      - `state`: `str` - `'before market'`/`'at market'`/`'after market'`  

- `Check.last_market(self)`  
   + **Purpose**: Gets last recorded trade date from [](stock-watch-model.md) model
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Output**: `str` - Date string of format `'YYYY-MM-DD'`  

- `Check.find_the_last_day(self)`  
   + **Purpose**: Finds most recent valid trade date within 10-day window 
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Output**: `str`/`None` - Valid date string or `None` if none found  

- `Check.strdate(self)`  
   + **Purpose**: Returns current date as standardized string  
   + **Output**: `str` - `'YYYY-MM-DD'` format  

- `Check.is_history_updated(self)`  
   + **Purpose**: Verifies Redis historical data matches latest database record 
   + **Inputs**:  
     - `self`: <include from="repeatable-texts.topic" element-id="python-self"/> 
   + **Output**: `bool` - `True` if Redis and [](stock-watch-model.md) dates match  

## Data Sources
- Uses <include from="third-party-libraries-links.topic" element-id="python-redis"/> for historical date storage  
- Relies on `jalali` library for Persian calendar conversions  
- Integrates with [](stock-watch-model.md) model for trade date tracking  

## Timezone Handling
All methods assume:  
- Input times in Iran Standard Time (UTC+3:30)  
- Convert to UTC for timestamp generation  
- Market hours: 8:30 AM to 12:30 PM local time  
