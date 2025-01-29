# Wallet

This doc is a thorough explanation of the model `Wallet` which is located in `accounts/models.py`.
This django model is for storing a user's financial information on %product%; e.g. balance, income, etc.

## What does it inherit?

This class inherits `django.db.models.Model`. Django offers this class as a tool for defining a SQL database in python.
The documentation is available at <include from="third-party-libraries-links.topic" element-id="django.db.models"></include>.

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
        <td>user</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.one-to-one"/>
            (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td>:heavy_check_mark:</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>Each user can have <b>only one</b> profile and each profile must be mapped to 
            <b>exactly one</b> user, thus this field has a one-to-one relation with <code>User.</code>
        </td>
    </tr>
    <tr>
        <td>balance</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td> Contains the amount of money the wallet has.</td>
    </tr>
    <tr>
        <td>income</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Stores the amount of money the `balance` increases over #TODO intervals.</td>
    </tr>
    <tr>
        <td>address</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Stores wallet's address over the internet.</td>
    </tr>
    <tr>
        <td>nonce</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO.</td>
    </tr>
    <tr>
        <td>last_change</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Stores timestamp of the last time this database row was updated.</td>
    </tr>
</table>



## Methods

### get_wallet
  - **usage**: It gets a `user` in the input and finds it inside the `Wallet` objects. If it did not find any, 
    it would create the wallet. Also, if the `last_change` field wasn't updated for over 70 days, it would update 
    the `address`. 
  - **signature**: `get_wallet(cls, user: User)`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **user**: An object of `django.contrib.aut.user.User` to find the wallet of this user.
  - **output**: A `dict` containing `address`, `income`, and `balance` fields of the found wallet.

### create_address
  - **usage**: It is a recursive function for creating an address on USDT website #TODO. The recursive part is for 
    implementing a retry mechanism. It retries 3 times until it succeeds. It saves the address on `self`. Every address 
    is uniquely created by randomly creating `nonce` for this wallet, and it is also uniquely identifiable.
  - **signature**: `create_address(self, num: int) -> str`
  - **parameters**: 
     + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
     + **num**: Shows number of retires that already happened.
  - **output**: A string containing the address created on USDT website #TODO.

### check_deposits
  - **usage**: It contacts the USDT via unique address created by `nonce` field and acquire all the deposits on that website.
    It adds all the non-existing deposits to the `Deposit` database.
  - **signature**: `check_deposit(self) -> bool`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `bool` variable representing whether any new `Deposit` objects have been created or not.

### *Trivial Methods*

#### \_\_str\_\_
Returns `user.username`

#### get_gateway_base
Returns the domain of USDT website.
