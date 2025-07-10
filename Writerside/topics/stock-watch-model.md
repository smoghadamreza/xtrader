# StockWatch

This doc is a thorough explanation of the model `StockWatch` which is located in `data/models.py`.
This django model is for storing comprehensive stock market data including instrument details, trading metrics, and price information.

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"></include>

*Notes* 
- No column with `ForeignKey` type.
- No column with `unique=True`.

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_nullable</td>
        <td>description</td>
    </tr>
    <tr>
        <td>SymbolId</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<a href="fund-model.md"/>)</td>
        <td>:x:</td>
        <td>The `Fund` which this snapshot belongs to.</td>
    </tr>
    <tr>
        <td>InstrumentName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>All assets of the fund at that point of time.</td>
    </tr>
    <tr>
        <td>InstrumentTitle</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>Official full name of the financial instrument/security</td>
    </tr>
    <tr>
        <td>InstrumentCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Unique ticker symbol for the instrument (e.g., AAPL, MSFT)</td>
    </tr>
    <tr>
        <td>InstrumentStateCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Code representing trading status (A=Active, S=Suspended, etc.)</td>
    </tr>
    <tr>
        <td>InstrumentStateTitle</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Description of trading status (Active, Suspended, etc.)</td>
    </tr>
    <tr>
        <td>BaseQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Standard trading unit/board lot size for the instrument</td>
    </tr>
    <tr>
        <td>pd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Primary price data field (exact meaning depends on data source)</td>
    </tr>
    <tr>
        <td>zd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Numerical indicator field (exact meaning depends on data source)</td>
    </tr>
    <tr>
        <td>qd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Primary quantity/volume data field</td>
    </tr>
    <tr>
        <td>po1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Secondary price data field (often represents bid/ask prices)</td>
    </tr>
    <tr>
        <td>zo1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Secondary numerical indicator field</td>
    </tr>
    <tr>
        <td>qo1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Secondary quantity/volume data field</td>
    </tr>
        <tr>
        <td>pd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Secondary price data field (typically represents closing price or VWAP)</td>
    </tr>
    <tr>
        <td>zd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Numerical indicator for price type (1=regular, 2=auction, etc.)</td>
    </tr>
    <tr>
        <td>qd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total volume at the secondary price level</td>
    </tr>
    <tr>
        <td>po2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Price data for second order book level (ask price)</td>
    </tr>
    <tr>
        <td>zo2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Order book level indicator (2=second level)</td>
    </tr>
    <tr>
        <td>qo2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Volume available at second order book level</td>
    </tr>
    <tr>
        <td>pd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Tertiary price data field (typically represents high/low prices)</td>
    </tr>
    <tr>
        <td>zd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Numerical indicator for price range (1=daily, 2=weekly, etc.)</td>
    </tr>
    <tr>
        <td>qd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Volume at tertiary price level</td>
    </tr>
    <tr>
        <td>po3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Price data for third order book level (ask price)</td>
    </tr>
    <tr>
        <td>zo3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Order book level indicator (3=third level)</td>
    </tr>
    <tr>
        <td>qo3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Volume available at third order book level</td>
    </tr>
    <tr>
        <td>BuyGroupCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Number of institutional buyer groups in the market</td>
    </tr>
    <tr>
        <td>BuyGroupVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total shares purchased by institutional buyer groups</td>
    </tr>
    <tr>
        <td>BuyGroupVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of total volume from institutional buyer groups</td>
    </tr>
    <tr>
        <td>BuyFirmCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Number of brokerage firms with buy orders in the market</td>
    </tr>
        <tr>
        <td>BuyFirmVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total shares purchased by brokerage firms</td>
    </tr>
    <tr>
        <td>BuyFirmVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of total volume from brokerage firm buy orders</td>
    </tr>
    <tr>
        <td>BuyIndividualCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Number of individual retail buyers in the market</td>
    </tr>
    <tr>
        <td>BuyIndividualVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total shares purchased by individual retail investors</td>
    </tr>
    <tr>
        <td>BuyIndividualVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of total volume from retail investor buy orders</td>
    </tr>
    <tr>
        <td>SellFirmCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Number of brokerage firms with sell orders in the market</td>
    </tr>
    <tr>
        <td>SellFirmVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total shares sold by brokerage firms</td>
    </tr>
    <tr>
        <td>SellFirmVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of total volume from brokerage firm sell orders</td>
    </tr>
    <tr>
        <td>SellIndividualCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Number of individual retail sellers in the market</td>
    </tr>
    <tr>
        <td>SellIndividualVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total shares sold by individual retail investors</td>
    </tr>
    <tr>
        <td>SellIndividualVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of total volume from retail investor sell orders</td>
    </tr>
    <tr>
        <td>ClosingPrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Final trading price at market close</td>
    </tr>    
    <tr>
        <td>ClosingPriceVariation</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Absolute price change from previous closing price</td>
    </tr>    
    <tr>
        <td>ClosingPriceVariationPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage price change from previous closing price</td>
    </tr>    
    <tr>
        <td>CompanyName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Legal name of the issuing company</td>
    </tr>
    <tr>
        <td>ExchangeName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Name of the stock exchange where instrument is listed (e.g., NYSE, NASDAQ)</td>
    </tr>
    <tr>
        <td>ExchangeCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Short code identifying the exchange (e.g., 'XNAS' for NASDAQ)</td>
    </tr>
        <tr>
        <td>LastTradeDate</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Date of the most recent trade execution (YYYY-MM-DD format)</td>
    </tr>
    <tr>
        <td>FirstTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Opening price of the trading day (first executed trade price)</td>
    </tr>
    <tr>
        <td>LastTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Most recent executed trade price before market close</td>
    </tr>
    <tr>
        <td>ReferencePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Benchmark price used for calculating daily price limits and variations</td>
    </tr>
    <tr>
        <td>ReferencePriceVariation</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Absolute difference between current price and reference price</td>
    </tr>
    <tr>
        <td>ReferencePriceVariationPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage change between current price and reference price</td>
    </tr>
    <tr>
        <td>YearHighestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Highest traded price reached during the current calendar year</td>
    </tr>
    <tr>
        <td>YearLowestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Lowest traded price reached during the current calendar year</td>
    </tr>
    <tr>
        <td>MinimumOrderQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Smallest allowable order size (minimum lot size)</td>
    </tr>
    <tr>
        <td>MaximumOrderQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Largest allowable order size (maximum lot size)</td>
    </tr>
    <tr>
        <td>LowerPriceThreshold</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Minimum allowable trading price (circuit breaker lower limit)</td>
    </tr>
    <tr>
        <td>UpperPriceThreshold</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Maximum allowable trading price (circuit breaker upper limit)</td>
    </tr>
    <tr>
        <td>LowestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Lowest executed trade price of the current trading day</td>
    </tr>
    <tr>
        <td>HighestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Highest executed trade price of the current trading day</td>
    </tr>
    <tr>
        <td>PreviousDayPrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Closing price from the previous trading session</td>
    </tr>
    <tr>
        <td>TotalNumberOfSharesTraded</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Cumulative volume of shares traded during the current session</td>
    </tr>
        <tr>
        <td>TotalNumberOfTrades</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total count of executed trades during the current trading session</td>
    </tr>
    <tr>
        <td>TotalTradeValue</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total monetary value of all trades (volume × price) in base currency</td>
    </tr>
    <tr>
        <td>Eps</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Earnings Per Share (net income divided by outstanding shares)</td>
    </tr>
    <tr>
        <td>PricePerEarningGroup</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Average P/E ratio for the instrument's industry/sector group</td>
    </tr>
    <tr>
        <td>PricePerEarning</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Current Price-to-Earnings ratio (market price per share / EPS)</td>
    </tr>
    <tr>
        <td>FreeFloatPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Percentage of shares available for public trading (not held by insiders)</td>
    </tr>
    <tr>
        <td>MonthAverageVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>30-day moving average of daily trading volume</td>
    </tr>
    <tr>
        <td>InstrumentMarketValue</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total market capitalization (current price × total shares outstanding)</td>
    </tr>
    <tr>
        <td>NumberOfSharesOrBonds</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>Total quantity of shares/bonds outstanding for the instrument</td>
    </tr>
</table>

## Methods

### __str__
  - **usage**: Returns the primary string representation of the instrument object, which is its unique `SymbolId`. Useful for debugging and display purposes in user interfaces or logs within trading platforms.
  - **signature**: __str__(self) -> str
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A string value representing the `SymbolId` of the instrument.

### to_dict
  - **usage**: Converts the instrument object into a dictionary format containing only the `SymbolId`. This can be used for lightweight serialization or passing basic identity data.
  - **signature**: to_dict(self) -> dict
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A dictionary with a single key `SymbolId` mapping to the instrument's identifier.

### dict
  - **usage**: Returns a dictionary of selected attributes from the instrument object, only if its `LastTradeDate` matches the provided date. Can be used for time-specific data filtering in trading systems.
  - **signature**: dict(self, keys: list, date: str) -> Union[dict, str]
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **keys**: A list of attribute names to include in the result dictionary.
    + **date**: The date to match against the instrument’s `LastTradeDate`.
  - **output**: A dictionary of selected attributes if the date matches, otherwise returns the string `'wrong symbol'`.

### as_json
  - **usage**: Serializes the instrument object into a JSON-like dictionary with human-readable and frontend-friendly field names. Useful for API responses in trading applications.
  - **signature**: as_json(self) -> dict
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A dictionary with fields including `symbol_id`, `kind`, `category`, `symbol_name`, `name`, `description`, and a placeholder `title`.

### read
  - **usage**: Reads all public fields of the instrument object and returns them as a dictionary. Converts numerical values to floats and represents others as strings. If a field value is `None`, it is returned as `0`. Useful for data processing or exporting instrument metadata.
  - **signature**: read(self) -> dict
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A dictionary containing all non-private attributes of the object with appropriate type conversions for use in analytics or external systems.

