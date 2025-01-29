# Deposit

This doc is a thorough explanation of the model `Deposit` which is located in `accounts/models.py`.
This django model is for storing a user's deposit transaction on the remote site of USDT and synchronize its content
with there.

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
        <td>wallet</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="accounts-wallet-model.md"/>)</td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>Maps each deposit to a corresponding wallet.</td>
    </tr>
    <tr>
        <td>address_in</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The address where deposit should be added to.</td>
    </tr>
    <tr>
        <td>address_out</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The address where deposit should be deducted from. #TODO</td>
    </tr>
    <tr>
        <td>txid_in</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Transaction (tx) id for in(?) #TODO</td>
    </tr>
    <tr>
        <td>txid_out</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Transaction (tx) id for out(?) #TODO</td>
    </tr>
    <tr>
        <td>init_amount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Initial balance of wallet before transaction. #TODO</td>
    </tr>
    <tr>
        <td>final_amount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Final balance of wallet after transaction. #TODO</td>
    </tr>
    <tr>
        <td>result</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Whether transaction succeeded or not. #TODO</td>
    </tr>
    <tr>
        <td>coin</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>The coin text itself. #TODO</td>
    </tr>
    <tr>
        <td>network</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>network #TODO</td>
    </tr>
    <tr>
        <td>tx_time</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Stores timestamp of the transaction time.</td>
    </tr>
</table>



## Methods

### create
  - **usage**: Gets required parameters for creating a `Deposit`. Finds the corresponding `Wallet` for it.
    Updates the `Wallet` attributes including `balance`. Creates the desired `Deposit`. Returns `True` if deposit was made 
    otherwise returns `False`.
  - **signature**: `create(cls, nonce: str, params: dict, wallet: Wallet) -> bool`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **nonce**: A unique token for finding a `Wallet` and its address on USDT website.
    + **params**: Fields of `Deposit` are saved as key-values in a `dict`. 
      Note they are not full processed and need some cleaning for some fields..
    + **wallet**: A [](accounts-wallet-model.md) object.
  - **output**: A `bool` representing whether the `Deposit` was created or not.

### get_deposits
  - **usage**: Given a `Wallet` in its input, finds the corresponding `Deposits` and returns them. Note that only a subset 
    fields of the `Deposit` is returned.
  - **signature**: `get_deposits(cls, wallet: Wallet) -> List<dict>`
  - **parameters**: 
     + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
     + **wallet**: A [](accounts-wallet-model.md) object.
  - **output**: A list of `dict` with custom fields where each would represent a `Deposit` for the input `Wallet`. 
