# Strategy

## Core Components

### Strategy Operations

- `add_strategy_to_db(data, user)`  
  + **Purpose**: Creates/updates strategy records with subscription validation  
  + **Inputs**:  
       - `data`: `dict` - Contains:  
           - `name`: `str` - Strategy name  
           - `filters`: `str` - JSON-stringified filter configurations  
           - `interval`: `str` - Analysis timeframe  
           - `watchlistId`: `str` - '0' for default or valid Watchlist ID  
           - `id`: `int` - Existing strategy ID (for updates)  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
  + **Output**: `dict` with:  
       - `result`: `str` - 'save'|'delete' operation status  
       - `id`: `int` - Strategy database ID  
       - Error redirect if subscription limits exceeded  

- `load_strategy_names(user)`  
  + **Purpose**: Retrieves user's strategy metadata  
  + **Inputs**:  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
  + **Output**: `list` of `dicts` with `id` and `name` keys  

- `load_strategy_from_db(user, strategy_id)`  
  + **Purpose**: Loads complete strategy configuration  
  + **Inputs**:  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
       - `strategy_id`: `int` - Strategy database ID  
  + **Output**: `dict` with:  
       - `filters`: `list` - Deserialized filter configurations  
       - `watchlistId`: `str` - Associated watchlist identifier  
       - `interval`: `str` - Analysis timeframe  

### Subscription Management

- `get_pack_limit(user)`  
  + **Purpose**: Returns active subscription package limits  
  + **Inputs**:  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
  + **Output**: `dict` with:  
       - `strategy`: `int` - Max allowed strategies  
       - `watchlist`: `int` - Max allowed watchlists  

- `get_strategy_counts(user)`  
  + **Purpose**: Counts user's active strategies  
  + **Inputs**:  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
  + **Output**: `int` - Number of strategies  

- `get_watchlist_counts(user)`  
  + **Purpose**: Counts user's custom watchlists  
  + **Inputs**:  
       - `user`: <include from="third-party-libraries-links.topic" element-id="django-models.user"/> 
  + **Output**: `int` - Watchlist count  

## Data Flow
1. Strategy creation/update via `add_strategy_to_db()`:  
   - Validates against [](sales-app-models.md) limits  
   - Links to [](watchlist-model.md) when provided  
2. Configuration loading through `load_strategy_from_db()` deserializes filters  
3. Package limits enforced through real-time subscription checks  

## Error Handling
- Returns upgrade redirect when:  
  - Strategy count exceeds subscription limit  
  - Using custom watchlists without active subscription  

## Dependencies
- Uses [](strategy-model.md) model for storage  
- Integrates with [](subscription-model.md) for limit checks  
- Relies on <include from="third-party-libraries-links.topic" element-id="django-models.user"/> model for ownership tracking