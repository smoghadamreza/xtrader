# Income

This doc is a thorough explanation of the model `Income` which is located in `data/models.py`.
This django model is for storing #TODO.

## What does it inherit?

This class inherits `django.db.models.Model`. Django offers this class as a tool for defining a SQL database in python.
The documentation is available at <include from="third-party-libraries-links.topic" element-id="django.db.models"></include>.

## Fields

*Notes*
- There are no columns with `unique=True` attribute.

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_nullable</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>StockWatch</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="stock-watch-model.md"/>)</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>#TODO
        </td>
    </tr>
    <tr>
        <td>SymbolId</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td> #TODO.</td>
    </tr>
    <tr>
        <td>InstrumentName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>total_income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>gross_profit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO.</td>
    </tr>
    <tr>
        <td>operating_income_or_loss</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>interest_expense</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>income_before_tax</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>net_income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
</table>



## Methods

### read
  - **usage**: reads all the fields of an entry or row in the corresponding table and return it as a `dict`.
  - **signature**: `read(self) -> dict`
  - **parameters**: 
     + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` containing all the columns as keys and their value at the corresponding row as value.
