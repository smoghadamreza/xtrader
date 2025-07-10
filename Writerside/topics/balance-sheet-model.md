# BalanceSheet

This doc is a thorough explanation of the model `BalanceSheet` which is located in `data/models.py`.
This django model is for storing balance sheet financial data for companies.

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
        <td>References the StockWatch object this financial data belongs to, establishing a parent-child relationship.
        </td>
    </tr>
    <tr>
        <td>SymbolId</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The unique ticker symbol identifier for the financial instrument (e.g., 'AAPL' for Apple).</td>
    </tr>
    <tr>
        <td>InstrumentName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>NA</td>
        <td>The official name of the financial instrument or security.</td>
    </tr>
    <tr>
        <td>cash</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total cash and cash equivalents available to the company (in base currency units).</td>
    </tr>
    <tr>
        <td>net_receivables</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Accounts receivable minus allowance for doubtful accounts.</td>
    </tr>
    <tr>
        <td>short_term_investments</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Investments that mature within one year or can be liquidated quickly.</td>
    </tr>
    <tr>
        <td>total_current_assets</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Sum of all assets expected to be converted to cash within one year.</td>
    </tr>
    <tr>
        <td>inventory</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Value of raw materials, work-in-progress, and finished goods.</td>
    </tr>
    <tr>
        <td>long_term_investments</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Investments not expected to be liquidated within the current year.</td>
    </tr>
    <tr>
        <td>property_plant_and_equipment</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Net value of tangible fixed assets used in operations (after depreciation).</td>
    </tr>
    <tr>
        <td>intangible_assets</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Non-physical assets like patents, trademarks, and goodwill.</td>
    </tr>
    <tr>
        <td>total_assets</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Sum of all current and non-current assets owned by the company.</td>
    </tr>
    <tr>
        <td>accounts_payable</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Amounts owed to suppliers for goods/services purchased on credit.</td>
    </tr>
    <tr>
        <td>total_current_liabilities</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Obligations due within one year, including payables and short-term debt.</td>
    </tr>
    <tr>
        <td>total_liabilities</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Sum of all current and long-term financial obligations.</td>
    </tr>
    <tr>
        <td>capital</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total paid-in capital from shareholders (common and preferred stock).</td>
    </tr>
    <tr>
        <td>retained_earnings</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Cumulative net earnings not distributed as dividends.</td>
    </tr>
    <tr>
        <td>equity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total shareholders' equity (assets minus liabilities).</td>
    </tr>
    <tr>
        <td>prepayment</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Payments made in advance for goods/services to be received in future periods.</td>
    </tr>
</table>


## Methods

### read
  - **usage**: reads all the fields of an entry or row in the corresponding table and return it as a `dict`.
  - **signature**: `read(self) -> dict`
  - **parameters**: 
     + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` containing all the columns as keys and their value at the corresponding row as value.
