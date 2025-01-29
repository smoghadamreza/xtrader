# Payment

The `Payment` class represents a purchase of  [](subscription-model.md). 

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"/>

*Notes*
- No field has `unique=True` attribute.
- All fields are nullable.

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>user</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user associated with this payment.</td>
    </tr>
    <tr>
        <td>action</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The action or type of payment. Defaults to an empty string.</td>
    </tr>
    <tr>
        <td>amount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>N/A</td>
        <td>The amount of the payment in Rials #TODO. Defaults to <code>0</code>.</td>
    </tr>
    <tr>
        <td>reason</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The reason or description for the payment. Defaults to an empty string.</td>
    </tr>
    <tr>
        <td>insert_time</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-time-field"/></td>
        <td>N/A</td>
        <td>The timestamp when the payment was recorded. Defaults to the current time.</td>
    </tr>
    <tr>
        <td>txid</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>N/A</td>
        <td>The transaction ID associated with the payment. Defaults to an empty string.</td>
    </tr>
</table>

## Methods

### pay
  - **usage**: Creates a `Payment` object according to the parameters of the input.
  - **signature**: `pay(cls, wallet: Wallet, amount: int, action: str, reason: str, pay2ref=True, txid: str) -> bool`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **wallet**: The [](accounts-wallet-model.md) which this payment affects.
    + **amount**: amount of payment.
    + **action**: The action which the payment represent, e.g. `pay`, `income`, and `receive`.
    + **reason**: The reason of payment.
    + **pay2ref**: If `True` the payment is deducted from this wallet to the wallet of the user which referred this user.
    + **txid**: Transaction id.
  - **output**: A `bool` which represents whether the payment was successful or not.
