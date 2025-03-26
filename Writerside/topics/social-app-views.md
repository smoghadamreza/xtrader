# Views

<include from="repeatable-texts.topic" element-id="django-views">
</include>

## Functions

### `protraders`

This function handles ProTrader account creation and retrieval.

#### Used Decorators {id=used_decorator_1}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_1}
- request: Standard Django HttpRequest object
- POST data requires:
  - username: Trader's username
  - brand: Brand identifier
  - page_kind: Page type
  - page_url: Page URL
  - subscription: Subscription details

#### Behavior {id=behavior_1}
- POST Requests:
  - Creates new ProTrader account
  - Validates trader existence
  - Gets exchange connection
  - Creates Pro account through OMS
  - Returns ProTrader ID or error

- GET Requests:
  - Checks for active follow relationship
  - Returns all ProTraders data
  - Includes current user's ProTrader status

- Error Handling:
  - Returns JSON error responses
  - Captures and reports exceptions

### `follow_unfollow`

This function handles following/unfollowing ProTraders for copy trading.

#### Used Decorators {id=used_decorator_2}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_2}
- request: Standard Django HttpRequest object
- POST data requires:
  - protrader_brand: Brand identifier of ProTrader
  - action: Either 'follow' or 'unfollow'

#### Behavior {id=behavior_2}
- POST Requests:
  - Processes follow/unfollow actions
  - Uses Follow.copytrade() for core logic
  - Requires authenticated user
  - Returns operation result

- Non-POST Requests:
  - Returns default OK response
  - No action performed

- Security:
  - Requires login via decorator
  - CSRF protection exempted

### `getpublics`

This function retrieves public keys of all ProTraders' exchanges.

#### Used Decorators {id=used_decorator_3}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_3}
- request: Standard Django HttpRequest object

#### Behavior {id=behavior_3}
- Retrieves all ProTrader records
- For each ProTrader:
  - Finds associated exchange
  - Collects exchange public key if exists
- Returns JSON array containing:
  - ProTrader IDs
  - Corresponding public keys
- No authentication required
- Bypasses CSRF protection

### `copy_order`

This function handles copying of trading orders from ProTraders.

#### Used Decorators {id=used_decorator_4}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="transaction-atomic-decorator"></include>

#### Input Parameters {id=input_param_4}
- request: Standard Django HttpRequest object
- POST data requires:
  - id: ProTrader ID
  - order: Order details to copy

#### Behavior {id=behavior_4}
- POST Requests:
  - Validates ProTrader existence
  - Executes order copy within atomic transaction
  - Returns success/error message
- Non-POST Requests:
  - Returns default OK response
- Security:
  - Atomic database transaction
  - CSRF protection exempted

### `promote`

This function handles user account promotion to ProTrader status.

#### Used Decorators {id=used_decorator_5}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_5}
- request: Standard Django HttpRequest object
- POST data requires:
  - brand: Display name for ProTrader
  - subscription: Subscription amount

#### Behavior {id=behavior_5}
- POST Requests:
  - Validates 7 requirements:
    1. Connected Binance account
    2. Linked Telegram account
    3. Unique brand name
    4. Not following others
    5. No existing ProTrader status
    6. Minimum 30-day trading history
    7. No pending promotion
  - Creates PENDING ProTrader entry
  - Notifies admin via Telegram
- Non-POST Requests:
  - Returns 403 error
- Security:
  - Requires authenticated user
  - CSRF protection exempted

### `trader`

This function renders the trader profile page.

#### Behavior {id=behavior_6}
- Renders [traderProfile.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/social/templates/traderProfile.html)
 template
- Uses get_user() helper to populate template context
- Returns standard Django HttpResponse
- No explicit authentication requirement
- Simple pass-through to template rendering

### `get_profile`

This function retrieves profile information for a specific ProTrader.

#### Input Parameters {id=input_param_7}
- request: Standard Django HttpRequest object
- pro_id: ID of the ProTrader profile to retrieve

#### Behavior {id=behavior_7}
- Validates ProTrader existence (returns redirect if invalid)
- Retrieves trading history records for the ProTrader
- Determines follow status for current user:
  - 0: Unknown/not logged in
  - 1: Actively following
  - 2: Not following
  - 3: Following someone else
- Returns JSON with:
  - ProTrader brand name
  - Subscription fee
  - Trading history
  - Current user's follow status
- Handles exceptions with redirect responses

### `copytrading`

This function renders the copy trading page for authenticated users.

#### Used Decorators {id=used_decorator_8}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_8}
- Requires user authentication (redirects to login page if not authenticated)
- Renders [copytrading.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/social/templates/copytrading.html)
 template
- Populates template context using get_user() helper function
- Returns standard Django HttpResponse

### `league`

This function renders the league landing page.

#### Behavior {id=behavior_9}
- Renders [leagueLanding.html](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/social/templates/leagueLanding.html) 
 template
- Uses get_user() helper to populate template context
- Returns standard Django HttpResponse
- No explicit authentication requirement
- Simple template rendering with user context

### `exchange`

This function handles exchange account management for authenticated users.

#### Used Decorators {id=used_decorator_10}
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_10}
- request: Standard Django HttpRequest object
- POST data requires:
  - public: Exchange API public key
  - secret: Exchange API private key
  - name: Exchange account name
  - exchange: Exchange platform identifier

#### Behavior {id=behavior_10}
- GET Requests:
  - Returns list of user's connected exchanges
- POST Requests:
  - Validates required API credentials
  - Verifies and creates new exchange connection
  - Returns verification status
- Error Handling:
  - Returns 400 for unsupported methods
  - Returns false status for invalid inputs
- Security:
  - Requires authenticated user
  - CSRF protection exempted
  - Handles sensitive API keys

