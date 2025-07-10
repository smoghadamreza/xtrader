# Fund

This doc is a thorough explanation of the model `Fund` which is located in `aum/models.py`.
This django model is for storing a mutual fund or investment portfolio's management data including assets, fees, and performance metrics.

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
        <td>manager</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>References the User account responsible for managing this fund. Multiple funds can be managed by the same user.</td>
    </tr>
    <tr>
        <td>issue_fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Percentage fee charged when investors purchase new fund units (typically 0.5-2% of investment amount).</td>
    </tr>
    <tr>
        <td>redeem_fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Percentage fee charged when investors sell fund units back to the fund (typically 0-1.5% of redemption amount).</td>
    </tr>
    <tr>
        <td>fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Annual management fee percentage charged against total assets under management (typically 0.1-2% per annum).</td>
    </tr>
    <tr>
        <td>aum</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Assets Under Management - total market value of all investments in the fund (in base currency).</td>
    </tr>
    <tr>
        <td>last_update</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Unix timestamp of when the fund's NAV and AUM were last calculated and updated.</td>
    </tr>
    <tr>
        <td>brand</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Brand name or marketing identifier for the fund (e.g., 'Global Growth Fund').</td>
    </tr>
    <tr>
        <td>deposit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total amount of new capital deposited into the fund during current reporting period.</td>
    </tr>
    <tr>
        <td>withdraw</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Total amount of capital withdrawn from the fund during current reporting period.</td>
    </tr>
</table>



## Methods

### get_units_count
  - **usage**: Calculates and returns sum of `FundInvestor.units` for all the instances of `FundInvestor` that are associated with this fund through the `fund` foreign key relationship.
  - **signature**: `get_units_count(self) -> int`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: Sum of all `units` that corresponds to this `Fund`. The `unit`s are stored on `FundInvestor` model.

### get_assets
  - **usage**: Gets one of `Exchange`s of this instance `manager` from `OMSManager` and retrieves the manager's portfolio holdings, returning a formatted list of assets with their current market values.
  - **signature**: `get_assets(self) -> List<Exchange>`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A list of `dict` with custom fields where each would represent an asset. 

### get_cash 
  - **usage**: Calculates the liquid cash value of specified assets (or all assets if none specified) in the fund's portfolio, converting holdings to their cash equivalents at current market rates. Updates the fund's cash position in the database.
  - **signature**: `get_cash(self, assets: List<dict>}) -> int`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **assets**: A list of dictionary which represent an assets. Determines which assets cash value should be calculated. 
      If it is `None`, all the assets will be evaluated.
  - **output**: Total cash value of the specified assets in base currency units.

### get_fund_info
  - **usage**: Returns all the info needed for review of this fund, including outputs of `get_units_count` and `get_cash`.
  - **signature**: `get_fund_info(self) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` with all the necessary information to view this `Fund`.

### get_transactions
  - **usage**: Gets all the deposits and withdrawals from `oms.Binance` exchange API, returns them as formatted transactions sorted chronologically, and synchronizes any new deposits with the fund's records.
  - **signature**: `get_transactions(self) -> List<dict>`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A list of `dict` with custom fields where each would represent a transaction. 

### issue_redeem
  - **usage**: Handles both issuance of new fund units to investors and redemption of existing units, applying the appropriate fees and updating investor balances accordingly.
  - **signature**: `issue_redeem(self, investor: FundInvestor, params: dict) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **investor**: The [](fund-investor-model.md) object.
    + **params**: A `dict` containing 'action' (issue/redeem), 'amount', and other transaction details.
  - **output**: A `dict` containing transaction status and details.

### get_unit_assets
  - **usage**: Creates a `dict` where keys are assets and each value represent unit worth of an asset.
  - **signature**: `issue_redeem(self, investor: FundInvestor, params: dict) -> dict`
  - **parameters**: 
    + **investor**: The [](fund-investor-model.md) object.
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` to show unit worth of each asset.

### create_snapshot
  - **usage**: Creates a snapshot of the `Fund`'s assets overall value from given offset until now. It is saved on `FundUnitSnapshot` model for historical performance tracking and reporting.
  - **signature**: `create_snapshots(self, assets: dict, history: int) -> None`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **assets**: List of `dict`s where each represent an asset.
    + **history**: The offset which shows start of the snapshot.

### fund_daily_snapshot
  - **usage**: Checks if no snapshot is created in the last day, creates one. 
  - **signature**: `fund_daily_snapshot(self) -> None`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />

### get_daily_snapshots
  - **usage**: Used for creating daily snapshots. If no snapshots created already, calls `init_fund_performance`.
  - **signature**: `get_daily_snapshots(cls) -> None`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />

### get_fund_performance
  - **usage**: Returns overall performance of the `Fund` by examining its corresponding snapshots overtime. returns the
    results from the given history offset.
  - **signature**: `get_fund_performance(self, mode: str, history: int)-> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **mode**: reports performance based on snapshots by value "fund", reports bitcoin prices by value "btc", and both by value "all".
    + **history**: The offset to count the entries from now to that offset. Report the result from offset until now.

### *Trivial Methods*

#### unit_transfer
Creates a `UnitTransfer` object to record transfers of fund units between investors or accounts.

### init_fund_performance
Calls `create_snapshot` if the wanted snapshot already doesn't exist. Returns proper message.
