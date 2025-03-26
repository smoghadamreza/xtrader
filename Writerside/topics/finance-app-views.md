# Views

<include from="repeatable-texts.topic" element-id="django-views">
</include>

## Functions

### `calculate_indicators`

This function calculates technical indicators for market data.

#### Input Parameters {id=input_param_1}
- request: Standard Django HttpRequest
- interval: Time interval string
- GET parameter 'param' with calculation specs

#### Behavior {id=behavior_1}
- Dynamically selects indicator function
- Processes data with given interval
- Returns JSON-formatted results

### `add_new_watch_list`

This function creates new trading watchlists.

#### Used Decorators {id=used_decorator_2}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_2}
- request: Standard Django HttpRequest
- POST data with watchlist name

#### Behavior {id=behavior_2}
- Validates subscription limits
- Checks for duplicate names
- Creates new watchlist record
- Returns creation status

### `get_watch_lists`

This function manages watchlist retrieval.

#### Used Decorators {id=used_decorator_3}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_3}
- request: Standard Django HttpRequest
- Optional GET parameters for filtering

#### Behavior {id=behavior_3}
- Returns all user watchlists
- Handles watchlist deletion
- Includes default watchlist
- Returns symbol lists when requested

### `update_symbol2watchlist`

This function modifies watchlist contents.

#### Used Decorators {id=used_decorator_4}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_4}
- request: Standard Django HttpRequest
- GET parameters for symbol operations

#### Behavior {id=behavior_4}
- Adds/removes symbols from watchlists
- Validates watchlist ownership
- Prevents default watchlist modification
- Returns operation status

### `save_strategy`

This function stores trading strategies.

#### Used Decorators {id=used_decorator_5}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_5}
- request: Standard Django HttpRequest
- POST parameter 'param' with strategy data

#### Behavior {id=behavior_5}
- Parses strategy configuration
- Saves to database
- Returns save result
- CSRF exempt for external integrations

### `get_strategy_names`

This function retrieves saved strategy names.

#### Behavior {id=behavior_6}
- Loads strategy names for current user
- Returns JSON list of strategy names
- No authentication required

### `load_strategy`

This function loads a specific trading strategy.

#### Input Parameters {id=input_param_7}
- request: Standard Django HttpRequest
- GET parameter 'id' with strategy ID

#### Behavior {id=behavior_7}
- Validates strategy ownership
- Loads strategy configuration
- Returns JSON-formatted filters
- Handles invalid IDs gracefully

### `scan_market`

This function executes market scans.

#### Input Parameters {id=input_param_8}
- request: Standard Django HttpRequest
- GET parameter 'strategyId'

#### Behavior {id=behavior_8}
- Runs market scan with specified strategy
- Returns JSON-formatted results
- Handles missing strategy ID

### `strategy_notif`

This function initiates strategy notifications.

#### Used Decorators {id=used_decorator_9}
<include from="repeatable-texts.topic" element-id="transaction-atomic-decorator"></include>

#### Input Parameters {id=input_param_9}
- request: Standard Django HttpRequest
- interval: Notification interval

#### Behavior {id=behavior_9}
- Starts background screening thread
- Handles daily snapshots for 1d interval
- Returns immediate success response

### `update_indicators`

This function updates indicator values.

#### Input Parameters {id=input_param_10}
- request: Standard Django HttpRequest
- GET parameter 'param' with update data

#### Behavior {id=behavior_10}
- Processes indicator update request
- Returns updated values
- Rejects non-GET requests

### `market_watch`

This function renders the market watch page.

#### Used Decorators {id=used_decorator_11}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_11}
- Checks subscription expiry status
- Renders payment page if expired
- Shows [marketwatch.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/marketwatch.html)
 for active subscriptions
- Includes user context data

### `display`

This function renders the trading backtest page.

#### Used Decorators {id=used_decorator_12}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_12}
- Sets default SymbolId (BTCUSDT)
- Includes user context data
- Renders [back.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/back.html)
 template
- Previously had subscription check logic

### `getfilters`

This function provides filter data.

#### Behavior {id=behavior_13}
- Returns pre-defined filter data
- No authentication required
- Simple HttpResponse with JSON
- No input parameters processed

### `filtermarket`

This function filters market data.

#### Input Parameters {id=input_param_14}
- request: Standard Django HttpRequest
- GET parameter 'filters' with criteria
- Optional 'page' parameter

#### Behavior {id=behavior_14}
- Applies filters to market data
- Implements pagination (10 items/page)
- Handles invalid page numbers
- Returns rendered HTML table

### `indicators_api`

This function provides indicator API data.

#### Behavior {id=behavior_15}
- Returns indicator group configurations
- Only accepts GET requests
- JSON response with API specs
- No authentication required

### `back_test`

This function executes strategy backtesting.

#### Input Parameters {id=input_param_16}
- request: Standard Django HttpRequest
- GET parameter 'param' with test data

#### Behavior {id=behavior_16}
- Parses backtest configuration
- Executes backtest simulation
- Returns performance results
- Rejects non-GET requests

### `about_us`

This function renders about page.

#### Behavior {id=behavior_17}
- Simple template rendering
- Includes username in context
- No authentication required
- Returns [aboutus.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/aboutus.html)

### `index`

This function handles root page.

#### Used Decorators {id=used_decorator_18}
<include from="repeatable-texts.topic" element-id="transaction-atomic-decorator"></include>

#### Behavior {id=behavior_18}
- Processes referral codes
- Sets session ref_id if valid
- Renders [newindex.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/newindex.html)
- Previously had login form logic

### `stockwatch`

This function redirects stockwatch.

#### Used Decorators {id=used_decorator_19}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_19}
- Redirects to /spot/BTCUSDT by default
- Handles empty SymbolId
- Previously rendered [stockwatch1.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/stockwatch1.html)

### `spot`

This function renders spot trading page.

#### Used Decorators {id=used_decorator_20}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_20}
- symbol_id: Trading pair symbol

#### Behavior {id=behavior_20}
- Validates symbol through Binance API
- Redirects to BTCUSDT on error
- Renders [stockwatch1.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/stockwatch1.html) with context
- Includes user data and symbol info

### `get_user`

This function provides user context.

#### Behavior {id=behavior_21}
- Retrieves user profile data
- Formats user image URL
- Returns dict with name/img_url
- Used by multiple views

### `profile_setup`

This function renders setup page.

#### Behavior {id=behavior_22}
- Simple template rendering
- Includes user context data
- Returns [setup.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/setup.html)
- No authentication required

### `ssl`

This function handles SSL verification.

#### Behavior {id=behavior_23}
- Returns verification string
- No processing logic
- Simple HttpResponse
- Used for domain validation

### `redi`

This function handles root redirects.

#### Behavior {id=behavior_24}
- Simple redirect to root path ('/')
- No authentication required
- No parameters processed
- Returns redirect response

### `trade`

This function processes trade orders.

#### Used Decorators {id=used_decorator_25}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_25}
- request: Standard Django HttpRequest
- POST parameter 'order' with trade data

#### Behavior {id=behavior_25}
- Validates exchange connection
- Processes order through OMS
- Returns execution result
- Handles unconnected exchange case

### `portfo`

This function retrieves portfolio data.

#### Behavior {id=behavior_26}
- Gets exchange connection
- Fetches portfolio assets
- Returns JSON with asset data
- Handles missing exchange case

### `get_orders`

This function retrieves order history.

#### Input Parameters {id=input_param_27}
- request: Standard Django HttpRequest
- GET parameter 'symbol'

#### Behavior {id=behavior_27}
- Validates exchange connection
- Fetches orders for specified symbol
- Returns JSON order list
- Handles missing exchange case

### `account_status`

This function provides account status.

#### Behavior {id=behavior_28}
- Gets exchange balance
- Returns simplified account data
- Focuses on buying power
- Handles missing exchange case

### `cancelOrder`

This function cancels orders.

#### Input Parameters {id=input_param_29}
- request: Standard Django HttpRequest
- GET parameters:
  - symbol
  - OrderId

#### Behavior {id=behavior_29}
- Validates exchange connection
- Cancels specified order
- Returns success/failure
- Handles missing exchange case

### `editOrder`

This function handles order edits.

#### Behavior {id=behavior_30}
- Placeholder implementation
- Returns default response
- Currently non-functional
- Reserved for future use

### `test_volume`

This function renders volume test page.

#### Behavior {id=behavior_31}
- Sets default SymbolId
- Includes user context
- Renders [test_volume.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/test_volume.html)
- No complex logic

### `manage_volume`

This function processes volume tests.

#### Input Parameters {id=input_param_32}
- request: Standard Django HttpRequest
- GET parameter 'param' with test data

#### Behavior {id=behavior_32}
- Executes volume test
- Returns test results
- Renders [volumetest.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/volumetest.html)
- Processes test parameters

### `testAPI`

This function renders API test page.

#### Behavior {id=behavior_33}
- Simple template render
- Sets default SymbolId
- Returns [testAPI.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/finance/templates/testAPI.html)
- No authentication

### `get_exchanges`

This function lists user exchanges.

#### Behavior {id=behavior_34}
- Gets all user exchanges
- Returns JSON list
- Uses OMSManager
- No authentication

### `save_exchange`

This function stores exchange connections.

#### Used Decorators {id=used_decorator_35}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_35}
- request: Standard Django HttpRequest
- POST parameters:
  - public
  - secret
  - name
  - exchange

#### Behavior {id=behavior_35}
- Validates required parameters
- Creates new exchange record
- Returns verification status
- CSRF exempt

### `remove_exchange`

This function deletes exchange connections.

#### Used Decorators {id=used_decorator_36}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Behavior {id=behavior_36}
- Removes Binance exchange
- Returns operation status
- CSRF exempt
- Hardcoded to Binance

### `tradingview`

This function manages TradingView webhooks.

#### Used Decorators {id=used_decorator_37}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_37}
- GET: Returns webhook info
- POST: Updates trading/notification settings
- Creates new webhook if missing
- Requires authenticated user

### `tradingview_trade`

This function processes TradingView alerts.

#### Used Decorators {id=used_decorator_38}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_38}
- request: Standard Django HttpRequest
- token: Webhook authentication token

#### Behavior {id=behavior_38}
- GET: Returns verification message
- POST: Executes trading commands
- Handles percentage-based quantities
- Sends Telegram notifications

### `telegram_webhook`

This function processes Telegram bot messages.

#### Used Decorators {id=used_decorator_39}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Behavior {id=behavior_39}
- Processes activation codes
- Links Telegram accounts
- Sends response messages
- Returns operation status
