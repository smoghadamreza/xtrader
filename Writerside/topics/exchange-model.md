# Exchange

This model represents a trading strategy defined by a user.

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
        <td>trader</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user">)</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user who owns the exchange configuration.</td>
    </tr>
    <tr>
        <td>name</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>The name of the exchange. Defaults to <code>"myExchange"</code>.</td>
    </tr>
    <tr>
        <td>exchange</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>The exchange platform (e.g., <code>"BINANCE"</code>).</td>
    </tr>
    <tr>
        <td>public</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The public API key for the exchange.</td>
    </tr>
    <tr>
        <td>private</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The private API key for the exchange.</td>
    </tr>
</table>
