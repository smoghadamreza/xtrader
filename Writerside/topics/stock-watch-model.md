# StockWatch

This doc is a thorough explanation of the model `StockWatch` which is located in `data/models.py`.
This django model is for storing #TODO.

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
        <td>#TODO</td>
    </tr>
    <tr>
        <td>InstrumentCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>InstrumentStateCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>InstrumentStateTitle</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BaseQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>pd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qd1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>po1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zo1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qo1</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>pd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qd2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>po2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zo2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qo2</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>pd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qd3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>po3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>zo3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>qo3</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyGroupCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyGroupVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyGroupVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyFirmCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyFirmVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyFirmVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyIndividualCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyIndividualVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>BuyIndividualVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellFirmCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellFirmVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellFirmVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellIndividualCount</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellIndividualVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>SellIndividualVolumePercentage</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.float-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ClosingPrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>    
    <tr>
        <td>ClosingPriceVariation</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>    
    <tr>
        <td>ClosingPriceVariationPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>    
    <tr>
        <td>CompanyName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ExchangeName</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ExchangeCode</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>LastTradeDate</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>FirstTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>LastTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ReferencePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ReferencePriceVariation</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>ReferencePriceVariationPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>YearHighestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>YearLowestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>MinimumOrderQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>MaximumOrderQuantity</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>LowerPriceThreshold</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>UpperPriceThreshold</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>LowestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>HighestTradePrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>PreviousDayPrice</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>TotalNumberOfSharesTraded</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>TotalNumberOfTrades</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>TotalTradeValue</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>Eps</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>PricePerEarningGroup</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>PricePerEarning</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>FreeFloatPercent</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.decimal-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>MonthAverageVolume</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>InstrumentMarketValue</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
    <tr>
        <td>NumberOfSharesOrBonds</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.big-int-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>#TODO</td>
    </tr>
</table>

## Methods

*#TODO*
