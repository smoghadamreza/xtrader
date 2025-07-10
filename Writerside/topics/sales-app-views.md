# Views


<include from="repeatable-texts.topic" element-id="django-views">
</include>

## Functions

### `get_packages`

This function retrieves available subscription packages and current user subscription status.

#### Behavior {id=behavior_1}
- Fetches all active packages ordered by monthly price
- Formats package information using info() method
- Checks for active user subscription
- Returns JSON containing:
  - Available packages
  - Current user's package with expiry date
- Handles unsubscribed users with default `'همیشه'` expiry

### `subscribe`

This function handles new subscription requests.

#### Used Decorators {id=used_decorator_1}
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_1}
- request: Standard Django <include from="repeatable-texts.topic" element-id="http-request"/>  object
- Requires POST data with 'subscribe' parameter (package ID)

#### Behavior {id=behavior_2}
- Validates package existence and activity status
- Processes subscription through Subscription.subscribe()
- Returns operation result with status and message
- Handles invalid package ID with error response
- CSRF protection exempted for payment integration

### `packages_view`

This function renders the packages page.

#### Behavior {id=behavior_3}
- Renders packages.html template
- Simple view without additional context
- No authentication requirement
