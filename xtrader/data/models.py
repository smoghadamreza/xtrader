from django.db import models
from django.utils import timezone


class StockWatch(models.Model):
    symbol_id = models.CharField(max_length=80)
    instrument_name = models.CharField(max_length=80)
    instrument_title = models.CharField(max_length=80)
    instrument_code = models.CharField(max_length=80, blank=True, null=True)
    instrument_state_code = models.CharField(
        max_length=50, blank=True, null=True
    )
    instrument_state_title = models.CharField(
        max_length=50, blank=True, null=True
    )
    base_quantity = models.BigIntegerField(blank=True, null=True)

    pd1 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zd1 = models.IntegerField(blank=True, null=True)
    qd1 = models.BigIntegerField(blank=True, null=True)
    po1 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zo1 = models.IntegerField(blank=True, null=True)
    qo1 = models.BigIntegerField(blank=True, null=True)
    pd2 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zd2 = models.IntegerField(blank=True, null=True)
    qd2 = models.BigIntegerField(blank=True, null=True)
    po2 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zo2 = models.IntegerField(blank=True, null=True)
    qo2 = models.BigIntegerField(blank=True, null=True)
    pd3 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zd3 = models.IntegerField(blank=True, null=True)
    qd3 = models.BigIntegerField(blank=True, null=True)
    po3 = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    zo3 = models.IntegerField(blank=True, null=True)
    qo3 = models.BigIntegerField(blank=True, null=True)

    buy_group_count = models.IntegerField(blank=True, null=True)
    buy_group_volume = models.BigIntegerField(blank=True, null=True)
    buy_group_volume_percentage = models.FloatField(blank=True, null=True)

    buy_firm_count = models.IntegerField(blank=True, null=True)
    buy_firm_volume = models.BigIntegerField(blank=True, null=True)
    buy_firm_volume_percentage = models.FloatField(blank=True, null=True)

    buy_individual_count = models.IntegerField(blank=True, null=True)
    buy_individual_volume = models.BigIntegerField(blank=True, null=True)
    buy_individual_volume_percentage = models.FloatField(blank=True, null=True)

    sell_firm_count = models.IntegerField(blank=True, null=True)
    sell_firm_volume = models.BigIntegerField(blank=True, null=True)
    sell_firm_volume_percentage = models.FloatField(blank=True, null=True)

    sell_individual_count = models.IntegerField(blank=True, null=True)
    sell_individual_volume = models.BigIntegerField(blank=True, null=True)
    sell_individual_volume_percentage = models.FloatField(
        blank=True, null=True
    )

    closing_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    closing_price_variation = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    closing_price_variation_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )

    company_name = models.CharField(max_length=50, blank=True, null=True)
    exchange_name = models.CharField(max_length=50, blank=True, null=True)
    exchange_code = models.CharField(max_length=50, blank=True, null=True)

    # TODO: change default value  to constant
    last_trade_data = models.DateField(
        default=timezone.now, blank=True, null=True
    )

    first_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    last_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )

    reference_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    reference_price_variation = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    reference_price_variation_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )

    year_highest_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    year_lowest_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )

    minimum_order_quantity = models.BigIntegerField(blank=True, null=True)
    maximum_order_quantity = models.BigIntegerField(blank=True, null=True)

    lower_price_threshold = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    upper_price_threshold = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )

    lowest_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    highest_trade_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )

    previous_day_price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True
    )
    total_number_of_shares_traded = models.BigIntegerField(
        blank=True, null=True
    )
    total_number_of_trades = models.BigIntegerField(blank=True, null=True)
    total_trade_value = models.BigIntegerField(blank=True, null=True)
    eps = models.IntegerField(blank=True, null=True)
    price_per_earning_group = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    price_per_earning = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    free_float_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    month_average_volume = models.BigIntegerField(blank=True, null=True)
    instrument_market_value = models.BigIntegerField(blank=True, null=True)
    number_of_shares_or_bonds = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.symbol_id

    def to_dict(self):
        obj_dict = {"symbol_id": self.symbol_id}
        return obj_dict

    def dict(self, keys, date):
        d = {}
        if str(self.last_trade_data) == date:
            for key in keys:
                try:
                    d[key] = float(self.__getattribute__(key))
                except Exception:
                    d[key] = self.__getattribute__(key)
            return d
        else:
            return "wrong symbol"

    def as_json(self):
        return dict(
            symbol_id=self.symbol_id,
            kind=self.instrument_state_title,
            category=self.exchange_name,
            symbol_name=self.instrument_name,
            name=self.company_name,
            description=self.company_name,
            title="title",
        )

    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != "_":
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value is None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class BalanceSheet(models.Model):
    stock_watch = models.ForeignKey(
        StockWatch, verbose_name="سهم ", on_delete=models.CASCADE
    )
    symbol_id = models.CharField(max_length=80, null=True, blank=True)
    instrument_name = models.CharField(max_length=80)
    cash = models.IntegerField(verbose_name="وجه نقد", null=True, blank=True)
    net_receivables = models.IntegerField(
        verbose_name="حساب های دریافتی", null=True, blank=True
    )
    short_term_investments = models.IntegerField(
        verbose_name="سرمایه های کوتاه مدت", null=True, blank=True
    )
    total_current_assets = models.IntegerField(
        verbose_name="دارایی های جاری ", null=True, blank=True
    )
    inventory = models.IntegerField(
        verbose_name="موجودی کالا", null=True, blank=True
    )
    long_term_investments = models.IntegerField(
        verbose_name="سرمایه گذاری بلند مدت", null=True, blank=True
    )
    property_plant_and_equipment = models.IntegerField(
        verbose_name="دادای های ثابت", null=True, blank=True
    )
    intangible_assets = models.IntegerField(
        verbose_name="دارایی های نامشهود", null=True, blank=True
    )
    total_assets = models.IntegerField(
        verbose_name="دارایی ", null=True, blank=True
    )
    accounts_payable = models.IntegerField(
        verbose_name="حساب های پرداختنی", null=True, blank=True
    )
    total_current_liabilities = models.IntegerField(
        verbose_name="بدهی جاری ", null=True, blank=True
    )
    total_liabilities = models.IntegerField(
        verbose_name="بدهی", null=True, blank=True
    )
    capital = models.IntegerField(verbose_name="سرمایه", null=True, blank=True)
    retained_earnings = models.IntegerField(
        verbose_name="سود انباشته", null=True, blank=True
    )
    equity = models.IntegerField(
        verbose_name="حقوق صاحبان سرمایه", null=True, blank=True
    )
    prepayment = models.IntegerField(
        verbose_name="پیش پرداخت", null=True, blank=True
    )

    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != "_":
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value is None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class Income(models.Model):
    stock_watch = models.ForeignKey(
        StockWatch, verbose_name="سهم ", on_delete=models.CASCADE
    )
    symbol_id = models.CharField(max_length=80, null=True, blank=True)
    instrument_name = models.CharField(max_length=80)
    total_income = models.IntegerField(
        verbose_name="فروش", null=True, blank=True
    )
    gross_profit = models.IntegerField(
        verbose_name="سود ناخالص", null=True, blank=True
    )
    operating_income_or_loss = models.IntegerField(
        verbose_name="سود عملیاتی", null=True, blank=True
    )
    interest_expense = models.IntegerField(
        verbose_name="هزینه های مالی ", null=True, blank=True
    )
    income_before_tax = models.IntegerField(
        verbose_name="سود قبل از مالیات", null=True, blank=True
    )
    net_income = models.IntegerField(
        verbose_name="سود خالص", null=True, blank=True
    )

    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != "_":
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value is None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class Ratio(models.Model):
    stock_watch = models.ForeignKey(
        StockWatch, verbose_name="سهم ", on_delete=models.CASCADE
    )
    symbol_id = models.CharField(max_length=80, null=True, blank=True)
    instrument_name = models.CharField(max_length=80)
    current_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="جاری",
        null=True,
        blank=True,
    )
    quick_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="آنی",
        null=True,
        blank=True,
    )
    cash_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="نقد",
        null=True,
        blank=True,
    )
    da = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="بدهی (درصد)",
        null=True,
        blank=True,
    )
    de = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="بدهی به ح ص س",
        null=True,
        blank=True,
    )
    sa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="گردش دارای (بار)",
        null=True,
        blank=True,
    )
    accounts_receivable_turnover_ratio = models.IntegerField(
        verbose_name="دوره گردش دریافتنی (روز)", null=True, blank=True
    )
    accounts_payable_turnover_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="حاشیه سود خالص (درصد)",
        null=True,
        blank=True,
    )
    inventory_turnover_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="دوره گردش موحودی ",
        null=True,
        blank=True,
    )
    profit_margin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="حاشیه سود خالص (درصد)",
        null=True,
        blank=True,
    )
    gross_profit_margin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="حاشیه سود ناخالص (درصد)",
        null=True,
        blank=True,
    )
    ebit_gross_profit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="سود عملیاتی به سود ناخالص (درصد)",
        null=True,
        blank=True,
    )
    r_ebit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="هزینه بهره به سود عملیاتی (درصد)",
        null=True,
        blank=True,
    )
    roa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="بازده دارایی (درصد)",
        null=True,
        blank=True,
    )
    roe = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="بازده ح ص س (درصد)",
        null=True,
        blank=True,
    )

    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != "_":
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value is None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class MarketWatch(models.Model):
    stock_watch = models.ForeignKey(
        StockWatch, null=True, blank=True, on_delete=models.CASCADE
    )
    balance_sheet = models.ForeignKey(
        BalanceSheet, null=True, blank=True, on_delete=models.CASCADE
    )
    ratio = models.ForeignKey(
        Ratio, null=True, blank=True, on_delete=models.CASCADE
    )
    income = models.ForeignKey(
        Income, null=True, blank=True, on_delete=models.CASCADE
    )

    def get_instrument_name(self):
        if self.stock_watch is None:
            raise ValueError("stock_watch is None")
        return self.stock_watch.instrument_name

    def get_symbol_id(self):
        if self.stock_watch is None:
            raise ValueError("stock_watch is None")
        return self.stock_watch.symbol_id

    def get_company_name(self):
        if self.stock_watch is None:
            raise ValueError("stock_watch is None")
        return self.stock_watch.company_name
