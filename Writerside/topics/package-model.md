# Package

The `Package` class represents a package or subscription plan in our system.
It can be bought by our users. #TODO

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
        <td>name</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>The name of the package. Labeled as <code>"نام پکیج"</code>.</td>
    </tr>
    <tr>
        <td>category</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The category of the package. Can be null or blank.</td>
    </tr>
    <tr>
        <td>price</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The price of the package. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>month_price</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The monthly price of the package. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>gas_fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The gas fee for the package. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>limit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The limit of the package. Defaults to <code>1</code>.</td>
    </tr>
    <tr>
        <td>days</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The number of days for the package. Defaults to <code>30</code>.</td>
    </tr>
    <tr>
        <td>active</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.boolean-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>Whether the package is active or not.</td>
    </tr>
    <tr>
        <td>description</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.text-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The description of the package. Defaults to an empty string.</td>
    </tr>
</table>

### *Trivial Methods*

#### \_\_str\_\_
Returns `self.name` + `str(self.price)`

#### info
Returns a dict containing a subset of the model's fields.
