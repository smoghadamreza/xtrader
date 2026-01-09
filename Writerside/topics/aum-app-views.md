# Views

<include from="repeatable-texts.topic" element-id="django-views">
</include>

## Functions

### `management`

This function renders the fund management page template for authenticated users.

#### Used Decorators {id=used_decorator_1}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>  

#### Input Parameters {id=input_param_1}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object

#### Behavior {id=behavior_1}
- Requires user authentication via decorator
- Renders the `fund_management.html` template
- Returns standard [HttpResponse](https://docs.djangoproject.com/en/5.1/ref/request-response/#httpresponse-objects) with rendered template

### `issue_redeem_unit`

This function handles unit issuance/redemption requests for fund managers.

#### Used Decorators {id=used_decorator_2}

<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>  

#### Input Parameters {id=input_param_2}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Expects JSON payload in POST body containing:
    - `investor_id`: ID of the investor
    - Other transaction parameters

#### Behavior {id=behavior_2}
- **POST Requests**:
  1. Validates manager authentication via decorator
  2. Parses JSON payload from request body
  3. Retrieves fund managed by current user
  4. Verifies investor belongs to fund
  5. Executes `issue_redeem` operation if valid
  6. Returns JSON response with operation result or error message
- **Non-POST Requests**:
  - Returns 403 error response
- Security:
  - Bypasses CSRF protection (via decorator)
  - Maintains data integrity through atomic fund/investor operations

### `redeem_unit`

This function handles unit redemption requests for authenticated users.

#### Used Decorators {id=used_decorator_3}

<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>  

#### Input Parameters {id=input_param_3}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Expects POST requests only

#### Behavior {id=behavior_3}
- **POST Requests**:
  1. Validates user authentication via decorator
  2. Returns simple success response (`{'msg': 'ok'}`)
- **Non-POST Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Security:
  - Bypasses CSRF protection (via decorator)
  - Only accessible to authenticated users

### `add_investor`

This function handles adding new investors to a fund by authenticated managers.

#### Used Decorators {id=used_decorator_4}

<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>  

#### Input Parameters {id=input_param_4}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Expects JSON payload in POST body containing:
    - `national_code`: Investor's national identification code
    - `first_name`: Investor's first name (max 20 chars)
    - `last_name`: Investor's last name (max 20 chars)
    - Other investor parameters

#### Behavior {id=behavior_4}
- **POST Requests**:
  1. Validates manager authentication via decorator
  2. Parses JSON payload from request body
  3. Checks for duplicate investors by national code
  4. Validates name length requirements (≤20 chars each)
  5. Creates new investor record if validation passes
  6. Returns appropriate JSON response:
     - Success (200)
     - Duplicate investor error
     - Name length validation error
- **Non-POST Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Security:
  - Bypasses CSRF protection (via decorator)
  - Restricts to fund managers only
  - Enforces data validation before creation

### `investors`

This function retrieves and returns a list of investors for the currently authenticated fund manager.

#### Used Decorators {id=used_decorator_5}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_5}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Only accepts GET requests

#### Behavior {id=behavior_5}
- **GET Requests**:
  1. Validates manager authentication
  2. Retrieves the fund associated with current user
  3. Fetches all investors belonging to the fund
  4. Formats investor data including:
     - ID
     - Full name (combined first and last name)
     - Unit holdings
     - National identification code
  5. Returns JSON response with investor list under 'data' key
- **Non-GET Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Data Handling:
  - Only returns investors for manager's own fund
  - Formats names in "First Last" format

### `get_fund`

This function retrieves and returns information about the fund managed by the currently authenticated user.

#### Used Decorators {id=used_decorator_6}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_6}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Only accepts GET requests

#### Behavior {id=behavior_6}
- **GET Requests**:
  1. Validates manager authentication
  2. Retrieves the fund associated with current user
  3. If fund exists:
     - Calls `get_fund_info()` method to gather fund data
  4. If no fund exists:
     - Returns empty object
  5. Returns JSON response with fund information
- **Non-GET Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Data Handling:
  - Only returns data for manager's own fund
  - Uses fund's built-in method for information gathering

### `transactions_history`

This function retrieves the transaction history for the fund managed by the currently authenticated user.

#### Used Decorators {id=used_decorator_7}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_7}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Only accepts GET requests

#### Behavior {id=behavior_7}
- **GET Requests**:
  1. Validates manager authentication
  2. Retrieves the fund associated with current user
  3. If fund exists:
     - Calls `get_transactions()` method to fetch transaction history
  4. Returns JSON response with transaction data under 'data' key
     - Returns empty array if no fund exists
- **Non-GET Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Data Handling:
  - Only returns transactions for manager's own fund
  - Wraps transaction data in {'data': [...]} structure

### `init_fund_performance`

This function initializes and returns fund performance data for authorized requests.

#### Used Decorators {id=used_decorator_8}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_8}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Requires GET parameter:
    - `pass`: Authorization token (must be 'XTreasury')

#### Behavior {id=behavior_8}
- **GET Requests**:
  1. Validates manager authentication
  2. Checks for valid authorization token
  3. If authorized:
     - Retrieves the fund associated with current user
     - Calls `init_fund_performance()` if fund exists
  4. Returns JSON response:
     - Performance data under 'data' key if successful
     - Empty array if no fund exists
     - 401 error if unauthorized
- **Non-GET Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Security:
  - Requires both authentication and special token
  - Only processes requests from fund manager

### `get_fund_performance`

This function retrieves performance data for the fund managed by the currently authenticated user.

#### Used Decorators {id=used_decorator_9}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Input Parameters {id=input_param_9}
- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/>  object
  - Accepts optional GET parameter:
    - `mode`: Performance data filter mode (default: 'all')

#### Behavior {id=behavior_9}
- **GET Requests**:
  1. Validates manager authentication
  2. Retrieves the fund associated with current user
  3. If fund exists:
     - Gets performance mode from request (defaults to 'all')
     - Calls `get_fund_performance()` with specified mode
  4. Returns JSON response:
     - Direct performance data array (safe=False)
     - Empty array if no fund exists
- **Non-GET Requests**:
  - Returns 403 error response with `{'msg': 'bad request'}`
- Data Handling:
  - Supports multiple performance view modes
  - Returns raw performance data without wrapper object
