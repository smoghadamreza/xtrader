# Jalali

## Core Components

### Gregorian to Persian Conversion
#### Gregorian Class
- `Gregorian.__init__(self, *date)`  
   + **Purpose**: Converts Gregorian dates to Persian (Jalali) calendar  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
        - `date`: Multiple input formats:  
            - `str` in `'YYYY-MM-DD'` format (e.g., `'2023-07-25'`)  
            - `datetime.date` object  
            - `tuple` of `(year, month, day)` as integers  
   + **Output**: Initializes instance with:  
        - `gregorian_year/month/day`: Original date components  
        - `persian_year/month/day`: Converted Jalali date components  

- `Gregorian.persian_tuple(self)`  
   + **Purpose**: Returns Persian date as numeric tuple  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
   + **Output**: `tuple` of `(year, month, day)` integers  

- `Gregorian.persian_string(self, date_format="{}-{}-{}")`  
   + **Purpose**: Formats Persian date as string  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
        - `date_format`: `str` - Python format string (default: `'{}-{}-{}'`)  
   + **Output**: `str` formatted date (e.g., `'1402-05-03'`)  

### Persian to Gregorian Conversion
#### Persian Class
- `Persian.__init__(self, *date)`  
   + **Purpose**: Converts Persian (Jalali) dates to Gregorian calendar  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
        - `date`: Multiple input formats:  
            - `str` in `'YYYY-MM-DD'` format (e.g., `'1402-05-03'`)  
            - `tuple` of `(year, month, day)` as integers  
   + **Output**: Initializes instance with:  
        - `persian_year/month/day`: Original Jalali components  
        - `gregorian_year/month/day`: Converted date components  

- `Persian.gregorian_tuple(self)`  
   + **Purpose**: Returns Gregorian date as numeric tuple  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
   + **Output**: `tuple` of `(year, month, day)` integers  

- `Persian.gregorian_string(self, date_format="{}-{}-{}")`  
   + **Purpose**: Formats Gregorian date as string  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
        - `date_format`: `str` - Python format string (default: `'{}-{}-{}'`)  
   + **Output**: `str` formatted date (e.g., `'2023-07-25'`)  

- `Persian.gregorian_datetime(self)`  
   + **Purpose**: Converts to Python standard date object  
   + **Inputs**:  
        - `self`: <include from="repeatable-texts.topic" element-id="python-self"/>  
   + **Output**: `datetime.date` object  

## Validation Rules
1. **Gregorian Inputs**:  
   - Uses `datetime.datetime` for validity checking  
   - Handles leap years automatically  

2. **Persian Inputs**:  
   - Rejects months >12 or days >31  
   - Forbids 31st day in months 7-12 (Jalali calendar rules)  
   - Uses regex pattern `r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$'` for string parsing  

## Conversion Logic
- Handles historical date ranges through custom epoch calculations  
- Accounts for different year cycles (132-year and 63-year patterns)  

## Dependencies
- Uses Python's standard `datetime` module for core date operations  
- Implements `re` module for string pattern matching  