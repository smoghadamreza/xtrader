# ProTrader

The `ProTrader` class represents a Professional Trader in %product% app. Professional in this context 
means a verified trader who meets platform requirements for performance, consistency, and risk management, and is 
approved to offer subscription services or copytrading to other users.

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"/>

*Notes*
- No field has `unique=True` attribute.
  - All fields are nullable.


## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>trader</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user">)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user account associated with this <code>ProTrader</code> profile.</td>
    </tr>
    <tr>
        <td>page_url</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The unique URL path for the <code>ProTrader</code>'s public profile page (e.g., '/traders/john-doe').</td>
    </tr>
    <tr>
        <td>page_kind</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The classification of trader profile (e.g., 'quantitative', 'technical', 'fundamental', 'crypto-specialist').</td>
    </tr>
    <tr>
        <td>brand</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The professional brand or trading style identifier (e.g., 'The Algorithmic Trader', 'Options Guru').</td>
    </tr>
    <tr>
        <td>subscription</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The monthly subscription fee amount (in base currency) for accessing this trader's signals/portfolio. Defaults to <code>0</code> for free accounts.</td>
    </tr>
    <tr>
        <td>age</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>N/A</td>
        <td>The number of months this trader has been active on the platform.</td>
    </tr>
    <tr>
        <td>nav</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>N/A</td>
        <td>The Net Asset Value of the trader's portfolio (in base currency units).</td>
    </tr>
    <tr>
        <td>beta</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The risk metric measuring portfolio volatility relative to the market (1.0 = market risk).</td>
    </tr>
    <tr>
        <td>one_year_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>Annualized percentage return of the trader's portfolio over the past year.</td>
    </tr>
    <tr>
        <td>six_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>Percentage return of the trader's portfolio over the past six months.</td>
    </tr>
    <tr>
        <td>three_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>Percentage return of the trader's portfolio over the past three months.</td>
    </tr>
    <tr>
        <td>one_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>Percentage return of the trader's portfolio over the past month.</td>
    </tr>
    <tr>
        <td>total_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>Cumulative percentage return since the trader joined the platform.</td>
    </tr>
    <tr>
        <td>status</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>Current account status.</td>
    </tr>
</table>

## Methods

### create_pro
  - **usage**: Initializes and stores historical performance-related attributes for a professional trading strategy based on exchange data. This method fetches historical NAV data using provided API credentials, sets the current state, and saves the instance. Used typically in setting up or updating a `ProTrader` profile.
  - **signature**: `create_pro(self, ex, ex_obj, brand=None, page_kind=None, page_url=None)`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **ex**: The exchange interface used to fetch historical NAV data. Must implement a `get_historical_nav` method.
    + **ex_obj**: An object containing `public` and `private` API credentials required for accessing exchange data.
    + **brand**: *(optional)* Branding information associated with the `ProTrader`, used for display or organizational purposes.
    + **page_kind**: *(optional)* Category or type of the profile or page representing this `ProTrader`.
    + **page_url**: *(optional)* URL linking to an external or internal page describing this `ProTrader`.
  - **output**: Returns the result of `ex.get_historical_nav()`, which is typically a list of historical NAV entries. Also sets and persists various attributes like `nav`, `age`, `brand`, and page metadata on the instance.

### get_history
  - **usage**: After finding [](exchange-model.md) object corresponding to this trader, it returns result of `get_historical_nav` function. The historical NAV data includes daily values with timestamps.
    - **signature**: `get_history(trader: django.contrib.auth.User)`
    - **parameters**: 
      + **trader**: The `User` which we want to get its historical NAV (Net Asset Value) reports.
    - **output**: The output of `get_historical_nav` function is a list of dictionaries containing date and NAV value pairs.

### get_records
  - **usage**: Gets bitcoin records of this `ProTrader` and returns it over time as a time-series of trade executions.
    - **signature** `get_records(trader: django.contrib.auth.User) -> dict`
    - **parameter**:
      + **trader**: The `User` which we want to get its records.
    - **output**: A `dict` with `trader` as its key and `btc` at its value, both of which are lists.

### get_all
  - **usage**: Returns all `ProTrader` objects with `status="Active"` attribute in a `list` of `dict`s where
    each `dict` has a custom subset of the `ProTrader` fields.
    - **signature**: `get_all(protrader_id: int) -> List<dict>`
    - **parameters**: 
      + **protrader_id**: The value which you would return in each dictionary as `protrader_id`.
    - **output**: A `list` of `dict` as described in usage section.

### copy_order
  - **usage**: Given an order, searches for all `Follow`s of this `Protrader` and 
    by using `OMSManager` copies this order to all followers' accounts with adjusted quantities based on their following ratios.
    - **signature**: ` copy_order(self, new_order) -> int`
    - **parameters**: 
       + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
      + **new_order**: The order to be copied.
    - **output**: Status code of the function. If it is `0` the function has failed.