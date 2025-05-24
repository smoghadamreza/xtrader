# Income

This doc is a thorough explanation of the model `Income` which is located in `data/models.py`.
This django model is for storing a user's income on a certain `symbol_id`.

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
        <td>corresponding `StockWatch` object.
        </td>
    </tr>
    <tr>
        <td>SymbolId</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td> The corresponding symbol which we evaluate income on.</td>
    </tr>
    <tr>
        <td>InstrumentName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>NA</td>
        <td>The symbol name.</td>
    </tr>
    <tr>
        <td>total_income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The total income which we evaluated.</td>
    </tr>
    <tr>
        <td>gross_profit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Profit after subtracting cost of goods sold (COGS) from total revenue.</td>
    </tr>
    <tr>
        <td>operating_income_or_loss</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Income from core business operations excluding taxes and interest.</td>
    </tr>
    <tr>
        <td>interest_expense</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Cost of borrowed funds or debt interest payments.</td>
    </tr>
    <tr>
        <td>income_before_tax</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total earnings before income taxes are deducted.</td>
    </tr>
    <tr>
        <td>net_income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Final profit after all expenses, taxes, and interest have been deducted.</td>
    </tr>
</table>



## Methods

### read
  - **usage**: reads all the fields of an entry or row in the corresponding table and return it as a `dict`.
  - **signature**: `read(self) -> dict`
  - **parameters**: 
     + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` containing all the columns as keys and their value at the corresponding row as value.
