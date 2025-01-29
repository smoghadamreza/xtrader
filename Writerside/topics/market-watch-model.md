# MarketWatch

This doc is a thorough explanation of the model `MarketWatch` which is located in `data/models.py`.
This django model is for storing #TODO.

## What does it inherit?

This class inherits `django.db.models.Model`. Django offers this class as a tool for defining a SQL database in python.
The documentation is available at <include from="third-party-libraries-links.topic" element-id="django.db.models"></include>.

## Fields

*Notes*
- There are no columns with `unique=True` attribute.
- All fields have `null=True` attribute.

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>stockWatch</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="stock-watch-model.md"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>#TODO
        </td>
    </tr>
    <tr>
        <td>balanceSheet</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="balance-sheet-model.md"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>#TODO
        </td>
    </tr>
    <tr>
        <td>ratio</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="ratio-model.md"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>#TODO
        </td>
    </tr>
    <tr>
        <td>income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="income-model.md"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>#TODO
        </td>
    </tr>
</table>



### *Trivial Methods*

#### get_instrument_name
Returns `self.stockWatch.InstrumentName`

#### get_SymbolId
Returns `self.stockWatch.SymbolId`

#### get_CompanyName
Returns `self.stockWatch.CompanyName`
