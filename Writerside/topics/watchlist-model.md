# WatchList

This model represents a user's watchlist, which contains a #TODO.

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
        <td>user</td> 
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td> 
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td> 
        <td>The user who owns the watchlist.</td> 
    </tr>
    <tr> 
        <td>name</td> 
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td> 
        <td>:heavy_check_mark:</td>
        <td>N/A</td> 
        <td>The name of the watchlist. Can be null or blank.</td> 
    </tr>
    <tr> 
        <td>updated</td> 
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-time-field"/></td> 
        <td>:heavy_check_mark:</td>
        <td>N/A</td> 
        <td>The timestamp when the watchlist was last updated. Defaults to the current time.</td> 
    </tr>
</table>

### *Trivial Methods*

#### \_\_str\_\_
Returns `self.user`: `self.name`


