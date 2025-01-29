# Ratio

This doc is a thorough explanation of the model `Ratio` which is located in `data/models.py`.
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
        <td>current_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>quick_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO.</td>
    </tr>
    <tr>
        <td>cash_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>da</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>de</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>sa</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>accounts_receivable_turnover_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>accounts_payable_turnover_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>inventory_turnover_ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>profit_margin</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>gross_profit_margin</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ebit_gross_profit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>r_ebit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>roa</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>roe</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
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
