# WatchListSymbol

This model represents a symbol within a user's watchlist.

## What does it inherit?

This class inherits `django.db.models.Model`. Django offers this class as a tool for defining a SQL database in python.
The documentation is available at <include from="third-party-libraries-links.topic" element-id="django.db.models"></include>.

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
        <td>watchlist</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<a href="watchlist-model.md"/>)</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The watchlist to which this symbol belongs.</td>
    </tr>
    <tr>
        <td>symbol</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The stock symbol. Can be null or blank.</td>
    </tr>
    <tr>
        <td>updated</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-time-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The timestamp when the symbol was last updated. Defaults to the current time.</td>
    </tr>
</table>

## Methods

#### get_symbols
  - **usage**: Used for getting symbol string of one or all `WatchListSymbol`s.
  - **signature**: `get_symbols(cls, watchlist_id: str) -> List<str>`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
  - **output**: List of all symbols if `watchlist_id` equals to zero, else symbol of the corresponding watchlist wrapped by a list. 
