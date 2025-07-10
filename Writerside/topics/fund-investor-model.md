# FundInvestor

This doc is a thorough explanation of the model `FundInvestor` which is located in `aum/models.py`.
This django model is for storing all investors of each `Fund` by all the necessary identification information. We also keep
number of `unit`s they invested on that `Fund`.

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
        <td>The `Fund` which this investor has invested on.</td>
    </tr>
    <tr>
        <td>nationalCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The national code of the investor.</td>
    </tr>
    <tr>
        <td>phoneNumber</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The phone number of the investor.</td>
    </tr>
    <tr>
        <td>first_name</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The first name of the investor.</td>
    </tr>
    <tr>
        <td>last_name</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The last name of the investor.</td>
    </tr>
    <tr>
        <td>note</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Any additional note on this investment should be written in this field. Mainly filled inside django-admin.</td>
    </tr>
    <tr>
        <td>units</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Number of units this investor has invested on the corresponding `Fund`.</td>
    </tr>
</table>
