# Strategy

This model represents a trading strategy defined by a user.

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"/>

*Notes*
- No field has `unique=True` attribute.

## Fields
<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_nullable</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>trader</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user who created the strategy.</td>
    </tr>
    <tr>
        <td>description</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>A description of the strategy.</td>
    </tr>
    <tr>
        <td>name</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>The name of the strategy. Defaults to <code>"استراتژی من"</code>.</td>
    </tr>
    <tr>
        <td>filters</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.text-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>The filters applied in the strategy.</td>
    </tr>
    <tr>
        <td>config</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>Configuration settings for the strategy.</td>
    </tr>
    <tr>
        <td>watch_list</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<a href="watchlist-model.md"/>)</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The watchlist associated with the strategy.</td>
    </tr>
    <tr>
        <td>interval</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The time interval for the strategy. Defaults to "4h".</td>
    </tr>
</table>

## Methods

#### loads
  - **usage**: returns a dict of `self` object with custom fields. Assumes there is a list in `filters`.
  - **signature**: `loads(self) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` with three fields `filters`, `interval`, and `symbols`. Calls `get_strategy_watchlist_symbols` for getting `symbols`.

#### get_strategy_watchlist_symbols
  - **usage**: For the corresponding `watch_list` of this object, calls [](watchlist-symbol-model.md)'s `get_symbols`.
  - **signature**: `get_strategy_watchlist_symbols(self) -> List<str>`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: Returns output of `get_symbols` function.
> Note: if `watch_list` is empty, we call `get_symbols` with `0` id which represents all symbols.

#### get_strategy_watchlist_id
  - **usage**: Get `self.watch_list.id`.
  - **signature**: `get_strategy_watchlist_id(self) -> int`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: For the corresponding `watch_list` of this object, returns its id. If `None` returns `0` which represents all watch_lists.

