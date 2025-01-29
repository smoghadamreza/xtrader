# Fund

This doc is a thorough explanation of the model `Fund` which is located in `aum/models.py`.
This django model is for storing a #TODO

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
        <td>#TODO</td>
    </tr>
    <tr>
        <td>issue_fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>redeem_fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>fee</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>aum</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>last_update</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>brand</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>deposit</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>withdraw</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>#TODO</td>
    </tr>
</table>



## Methods

### get_units_count
  - **usage**: Calculates and returns sum of `FundInvestor.units` for all the instances of `FundInvestor` #Todo
    that their `fund` field is equal to this object.
  - **signature**: `get_units_count(self) -> int`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: Sum of all `units` that corresponds to this `Fund`. The `unit`s are stored on `FundInvestor` model.

### get_assets
  - **usage**: Gets one of `Exchange`s of this instance `manager` from `OMSManager` #TODO and by using that `Exchange`, 
    gets `portfolio` of this `manager` and returns its assets.
  - **signature**: `get_assets(self) -> List<Exchange>`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A list of `dict` with custom fields where each would represent an asset. 

### get_cash 
  - **usage**:  #TODO Calculates the cash value of the given asset or all asset of this instance `manager`. 
   Returns the possible unit of cash. Updates this entry accordingly on the table.
  - **signature**: `get_cash(self, assets: List<dict>}) -> int`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **assets**: A list of dictionary which represent an assets. Determines which assets cash value should be calculated. 
      If it is `None`, all the assets will be evaluated.
  - **output**: Sum of all `units` that corresponds to this `Fund`. The `unit`s are stored on `FundInvestor` model.

### get_fund_info
  - **usage**: Returns all the info needed for review of this fund, including outputs of `get_units_count` and `get_cash`.
  - **signature**: `get_fund_info(self) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` with all the necessary information to view this `Fund`.

### get_transactions
  - **usage**: Gets all the deposits and withdraws from `oms.Binance` #TODO and returns a subset of their fields as a transaction 
    in a sorted by time manner. In the meanwhile, if we see a deposit that has not been updated into this `Fund` object, we update
    this transaction into the `Fund` as well.
  - **signature**: `get_transactions(self) -> List<dict>`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A list of `dict` with custom fields where each would represent a transaction. 

### issue_redeem
  - **usage**: #TODO
  - **signature**: `issue_redeem(self, investor: #TODO, params: dict) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **investor**: #TODO
    + **params**: A `dict` for finding proper action between redeem and issue.
  - **output**: A `dict` to show proper message in response to user action.

### get_unit_assets
  - **usage**: Creates a `dict` where keys are assets and each value represent unit worth of an asset.
  - **signature**: `issue_redeem(self, investor: #TODO, params: dict) -> dict`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `dict` to show unit worth of each asset.

### create_snapshot
  - **usage**: Creates a snapshot of the `Fund`'s assets overall value from given offset until now. It is saved on `FundUnitSnapshot`. #TODO
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
Creates a `UnitTransfer` object. #Todo.

### init_fund_performance
Calls `create_snapshot` if the wanted snapshot already doesn't exist. Returns proper message.

