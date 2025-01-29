# TraderHistory

The `TraderHistory` class represents trade history of a [](pro-trader-model.md) in %product%.

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
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<a href="pro-trader-model.md"/>)</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The trader associated with this history record.</td>
    </tr>
    <tr>
        <td>record_time</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The timestamp of the record. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>btc</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The BTC value associated with the record. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>nav</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The NAV (Net Asset Value) associated with the record. Defaults to <code>0</code>.</td>
    </tr>
</table>