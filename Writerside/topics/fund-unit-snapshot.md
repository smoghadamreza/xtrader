# FundUnitSnapshot

This doc is a thorough explanation of the model `FundUnitSnapshot` which is located in `aum/models.py`.
This django model is for storing snapshots of a `Fund` by custom attributes over time in order to provide 
overall observation of the `Fund` to the user.

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"></include>

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_unique</td>
        <td>is_nullable</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>fund</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="fund-model.md"/>)</td>
        <td>:x:</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The `Fund` which this snapshot belongs to.</td>
    </tr>
    <tr>
        <td>asset</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>All assets of the fund at that point of time.</td>
    </tr>
    <tr>
        <td>quantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>value</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>nav</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>insert_date</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>age</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
</table>
