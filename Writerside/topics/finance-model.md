# Finance

The **Finance** app is a Django-based trading automation and portfolio management platform
designed to streamline cryptocurrency trading. It integrates with external exchanges
([](exchange-model.md)) and TradingView alerts ([](trading-view-model.md)) to execute trades
based on user-defined strategies ([](strategy-model.md)).
Users can monitor market movements through customizable watchlists ([](watchlist-model.md) and [](watchlist-symbol-model.md)),
allowing them to track specific cryptocurrencies and trigger automated trading actions.

This app serves as a bridge between market analysis (via TradingView)
and execution (via exchange APIs), enabling systematic trading with minimal manual intervention.
By combining strategy configurations, real-time alerts, and exchange connectivity,
the **Finance** app provides traders with a structured approach to cryptocurrency investing
while maintaining control over risk parameters and trade automation.
