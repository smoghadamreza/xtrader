"""
scan_service.py

Encapsulates all market scanning logic that was formerly spread across finance/scan.py.
Handles threaded screening for all users, strategy-level scans, Telegram notifications,
wallet checks, and indicator computations.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from django.db import connections

from accounts.models import Profile, Wallet
from accounts.services import TelegramService
from data.models import StockWatch
from finance.models import Strategy
from finance.services import StrategyService, IndicatorService
from sales.models import Payment, Subscription
from utils.consts import TelegramMessage


class ScanService:
    """Handles market scanning across users and strategies."""

    def __init__(self, interval: str):
        self.interval = interval
        self.telegram_service = TelegramService()

    # -------------------------------------------------------------------------
    # PUBLIC METHODS
    # -------------------------------------------------------------------------

    def run_all_users(self) -> None:
        """Run market screener for all users."""
        users = set(strategy.trader for strategy in Strategy.objects.all())

        for user in users:
            profile = Profile.objects.filter(user=user).first()
            if not profile or not profile.telegram_id:
                continue

            strategy_service = StrategyService(trader=user)
            strategy_count = strategy_service.get_strategy_counts()
            strategy_limit = strategy_service.get_pack_limit().strategy

            if strategy_count > strategy_limit:
                self.telegram_service.send_message(
                    text=TelegramMessage.SUBSCRIPTION_ENDED,
                    chat_id=profile.telegram_id,
                )
                continue

            wallet = Wallet.objects.filter(user=user).first()
            strategies = Strategy.objects.filter(trader=user, interval=self.interval)
            for strategy in strategies:
                self._handle_user_strategy(profile, wallet, user, strategy)

        # Close all DB connections after threading starts
        for conn in connections.all():
            conn.close()

    def _scan_market(
        self,
        username: str,
        strategy_id: int,
        former: bool = False,
    ) -> Dict[str, Any]:
        """Scan the market for a single strategy (no threading)."""
        filters, interval, symbol_ids = self._find_strategy_filters(username, strategy_id)
        scan_result: Dict[str, List[Dict[str, str]]] = {"buy": [], "sell": []}

        for symbol_id in symbol_ids:
            result = self._evaluate_symbol(symbol_id, filters, interval, former)
            if result["buy"]:
                scan_result["buy"].extend(result["buy"])
            if result["sell"]:
                scan_result["sell"].extend(result["sell"])

        return scan_result

    # -------------------------------------------------------------------------
    # INTERNAL METHODS
    # -------------------------------------------------------------------------

    def _handle_user_strategy(
        self,
        profile: Profile,
        wallet: Wallet,
        user: User,
        strategy: Strategy,
    ) -> None:
        """Handle one user's strategy, wallet, and threading."""
        watchlist_id = strategy.get_strategy_watchlist_id()
        watchlist_name = "پیش فرض"

        if watchlist_id > 0:
            subscription = Subscription.have_subscribe(user=user)
            if not subscription:
                self.telegram_service.send_message(
                    text=TelegramMessage.SUBSCRIPTION_ENDED,
                    chat_id=profile.telegram_id,
                )
                return

            watchlist_name = strategy.watchlist.name
            strategy_params = strategy.loads()

            gas_fee = (
                len(strategy_params["filters"])
                * len(strategy_params["symbols"])
                * subscription.package.gas_fee
            )

            if not wallet or not Payment.pay(
                wallet=wallet,
                amount=gas_fee,
                action="pay",
                reason="اسکن بازار",
                pay2ref=True,
            ):
                self.telegram_service.send_message(
                    text=TelegramMessage.INSUFFICIENT_WALLET_FUND_FOR_MARKET_SCAN,
                    chat_id=profile.telegram_id,
                )
                return

        # Thread per strategy
        t = threading.Thread(
            target=self._scan_thread,
            args=(
                user.username,
                strategy.name,
                strategy.pk,
                profile.telegram_id,
                self.interval,
                watchlist_id,
                watchlist_name,
            ),
        )
        t.start()

    def _scan_thread(
        self,
        username: str,
        strategy_name: str,
        strategy_id: int,
        telegram_id: str,
        interval: str,
        watchlist_id: int,
        watchlist_name: str,
    ) -> None:
        """Execute scan and send Telegram message."""
        result = self._scan_market(username, strategy_id, former=False)
        msg = self._build_result_message(result, strategy_name, watchlist_name, interval, watchlist_id)
        self.telegram_service.send_message(text=msg, chat_id=telegram_id)

        # Prevent connection leaks
        for conn in connections.all():
            conn.close()

    # -------------------------------------------------------------------------
    # CORE LOGIC
    # -------------------------------------------------------------------------

    def _evaluate_symbol(
        self,
        symbol_id: str,
        filters: List[Dict[str, Any]],
        interval: str,
        former: bool,
    ) -> Dict[str, Any]:
        """Run all indicator filters for a single symbol."""
        scan_result = {"buy": [], "sell": []}

        first_dict, second_dict = {}, {}
        first, second, bad_symbol = False, False, False

        for idx, strategy_filter in enumerate(filters):
            strategy_filter["symbol_id"] = symbol_id
            try:
                result = self._calculate_filter_result(strategy_filter, interval)
            except Exception as e:
                print(f"[ScanService] Error in filter {idx} for {symbol_id}: {e}")
                bad_symbol = True
                continue

            if result["type"] == "first":
                first_dict[f"filter-first-{idx}"] = self._make_list_ready(result["result"])
                first = True
            elif result["type"] == "second":
                second_dict[f"filter-second-{idx}"] = self._make_list_ready(result["result"])
                second = True

        final_dict = {}
        if first:
            final_dict["first"] = self._check_first_kind(first_dict)
        if second:
            final_dict["second"] = self._check_second_kind(second_dict)

        if bad_symbol:
            return scan_result

        final = self._final_check(final_dict)
        if not former and final[-1] == final[-2]:
            return scan_result

        if final[-1] == 1:
            scan_result["buy"].append({"symbol_id": symbol_id})
        elif final[-1] == -1:
            scan_result["sell"].append({"symbol_id": symbol_id})

        return scan_result

    def _calculate_filter_result(self, strategy_filter: Dict[str, Any], interval: str) -> Dict[str, Any]:
        """Delegate to IndicatorService."""
        kind = strategy_filter["kind"].lower()
        symbol = strategy_filter["symbol_id"]

        service = IndicatorService(symbol=symbol, interval=interval)
        return service.give_result(strategy_filter, kind, get_json=False)

    # -------------------------------------------------------------------------
    # HELPER COMPUTATIONS (ported from old scan.py)
    # -------------------------------------------------------------------------

    def _check_first_kind(self, results: Dict[str, List[int]]) -> np.ndarray:
        df = pd.DataFrame(results)
        magic_number = len(results)
        result = df.sum(axis=1)
        check = result.apply(lambda x: 0 if -magic_number < x < magic_number else x)
        return np.asarray(check.replace([magic_number, -magic_number], [1, -1]))

    def _check_second_kind(self, results: Dict[str, List[int]]) -> np.ndarray:
        df = pd.DataFrame(results)
        return np.asarray(df.product(axis=1))

    def _final_check(self, final_dict: Dict[str, np.ndarray]) -> np.ndarray:
        df = pd.DataFrame(data=final_dict)
        return np.asarray(df.product(axis=1))

    def _make_list_ready(self, unready_list: str) -> List[int]:
        """Convert serialized result string to a clean list."""
        try:
            return [x[0] for x in eval(unready_list)]
        except Exception:
            return []

    # -------------------------------------------------------------------------
    # UTILITY
    # -------------------------------------------------------------------------

    def _find_strategy_filters(
        self,
        username: str,
        strategy_id: int,
    ) -> tuple[List[Dict[str, Any]], str, List[str]]:
        trader = User.objects.get_by_natural_key(username=username)
        strategy = Strategy.objects.get(trader=trader, id=strategy_id).loads()
        return strategy["filters"], strategy["interval"], strategy["symbols"]

    def _build_result_message(
        self,
        result: Dict[str, Any],
        strategy_name: str,
        watchlist_name: str,
        interval: str,
        watchlist_id: int,
    ) -> str:
        """Construct the Telegram message."""
        msg = (
            f"نتیجه اسکن بازار برای استراتژی {strategy_name}:\n"
            f"واچ‌لیست: {watchlist_name}\n"
            f"تایم‌فریم: {interval}\n"
        )

        if result["buy"]:
            msg += "سیگنال خرید:\n"
            for symbol in result["buy"]:
                msg += f"{symbol['symbol_id']}\nhttps://ramzservat.com/spot/{symbol['symbol_id']}\n"

        if result["sell"]:
            msg += "سیگنال فروش:\n"
            for symbol in result["sell"]:
                msg += f"{symbol['symbol_id']}\nhttps://ramzservat.com/spot/{symbol['symbol_id']}\n"

        if not result["buy"] and not result["sell"]:
            msg += "سیگنالی وجود ندارد\n"

        if watchlist_id == 0:
            msg += "کاربر گرامی با ارتقا اشتراک خود می‌توانید واچ‌لیست‌های شخصی و بیش از یک استراتژی بسازید."

        return msg
