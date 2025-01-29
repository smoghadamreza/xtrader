# ProTrader

The `ProTrader` class represents a Professional Trader in xtrader app. Professional in this context means #TODO.

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
        <td>The user associated with this <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>page_url</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The URL of the <code>ProTrader</code>'s page.</td>
    </tr>
    <tr>
        <td>page_kind</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The type or kind of the <code>ProTrader</code>'s page. #TODO</td>
    </tr>
    <tr>
        <td>brand</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The brand associated with the <code>ProTrader</code>. #TODO</td>
    </tr>
    <tr>
        <td>subscription</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The subscription value for the <code>ProTrader</code>. Defaults to <code>0</code>. #TODO what does it even mean?</td>
    </tr>
    <tr>
        <td>age</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>N/A</td>
        <td>The age of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>nav</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>N/A</td>
        <td>The NAV (Net Asset Value) of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>beta</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The beta value of the <code>ProTrader</code>. #TODO</td>
    </tr>
    <tr>
        <td>one_year_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The one-year performance metric of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>six_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The six-month performance metric of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>three_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The three-month performance metric of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>one_months_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The one-month performance metric of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>total_performance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The total performance metric of the <code>ProTrader</code>.</td>
    </tr>
    <tr>
        <td>status</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The status of the <code>ProTrader</code>. #TODO</td>
    </tr>
</table>

## Methods

### create_pro #TODO: it does not do what the name suggests.

### get_history
  - **usage**: After finding [](exchange-model.md) object corresponding to this trader, it returns result of `get_historical_nav` function. #TODO.
  - **signature**: `get_history(trader: django.contrib.auth.User)`
  - **parameters**: 
    + **trader**: The `User` which we want to get its historical NAV (Net Asset Value) reports.
  - **output**: The output of `get_historical_nav` #TODO function.

### get_records
  - **usage**: Gets bitcoin records of this `ProTrader` and returns it over time #TODO?.
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
    by using `OMSManager` copies this order. #TODO
  - **signature**: ` copy_order(self, new_order) -> int`
  - **parameters**: 
     + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **new_order**: The order to be copied.
  - **output**: Status code of the function. If it is `0` the function has failed.
