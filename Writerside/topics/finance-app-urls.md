# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**                                                                 | **View Function**               | **Function Documentation Link**                                         |
|---------------------------------------------------------------------------|---------------------------------|-------------------------------------------------------------------------|
| `^calculate_filter/(?:(?P<interval>\w+)/)?$`                              | `views.calculate_indicators`    | [calculate_indicators](finance-app-views.md#calculate-indicators)       |
| `^save_strategy`                                                          | `views.save_strategy`           | [save_strategy](finance-app-views.md#save-strategy)                     |
| `^get_strategy_names`                                                     | `views.get_strategy_names`      | [get_strategy_names](finance-app-views.md#get-strategy-names)           |
| `^load_strategy`                                                          | `views.load_strategy`           | [load_strategy](finance-app-views.md#load-strategy)                     |
| `^scan_market`                                                            | `views.scan_market`             | [scan_market](finance-app-views.md#scan-market)                         |
| `^updateSymbol2Watchlist`                                                 | `views.update_symbol2watchlist` | [update_symbol2watchlist](finance-app-views.md#update-symbol2watchlist) |
| `^addNewWatchList`                                                        | `views.add_new_watch_list`      | [add_new_watch_list](finance-app-views.md#add-new-watch-list)           |
| `^getWatchLists`                                                          | `views.get_watch_lists`         | [get_watch_lists](finance-app-views.md#get-watch-lists)                 |
| `^strategyNotif/(?:(?P<interval>\w+)/)?$`                                 | `views.strategy_notif`          | [strategy_notif](finance-app-views.md#strategy-notif)                   |
| `^marketwatch`                                                            | `views.market_watch`            | [market_watch](finance-app-views.md#market-watch)                       |
| `^getfilters`                                                             | `views.getfilters`              | [getfilters](finance-app-views.md#getfilters)                           |
| `^filtermarket`                                                           | `views.filtermarket`            | [filtermarket](finance-app-views.md#filtermarket)                       |
| `^indicators-api`                                                         | `views.indicators_api`          | [indicators_api](finance-app-views.md#indicators-api)                   |
| `^robots`                                                                 | `views.display`                 | [display](finance-app-views.md#display)                                 |
| `^back-test`                                                              | `views.back_test`               | [back_test](finance-app-views.md#back-test)                             |
| `^about-us`                                                               | `views.about_us`                | [about_us](finance-app-views.md#about-us)                               |
| `^$`                                                                      | `views.index`                   | [index](finance-app-views.md#index)                                     |
| `^stockwatch/(?:(?P<SymbolId>\w+)/)?$`                                    | `views.stockwatch`              | [stockwatch](finance-app-views.md#stockwatch)                           |
| `^spot/(?:(?P<symbol_id>\w+)/)?$`                                         | `views.spot`                    | [spot](finance-app-views.md#spot)                                       |
| `^.well-known/acme-challenge/S40flyGXu3pwdfdYzH-MLgUCromgJXv8WMbnAO_LXwE` | `views.ssl`                     | [ssl](finance-app-views.md#ssl)                                         |
| `^trade`                                                                  | `views.trade`                   | [trade](finance-app-views.md#trade)                                     |
| `^tradingview`                                                            | `views.tradingview`             | [tradingview](finance-app-views.md#tradingview)                         |
| `^webhook/(?P<token>[\w-]+)`                                              | `views.tradingview_trade`       | [tradingview_trade](finance-app-views.md#tradingview-trade)             |
| `^portfo`                                                                 | `views.portfo`                  | [portfo](finance-app-views.md#portfo)                                   |
| `^orders`                                                                 | `views.get_orders`              | [get_orders](finance-app-views.md#get-orders)                           |
| `^profile/setup/$`                                                        | `views.profile_setup`           | [profile_setup](finance-app-views.md#profile-setup)                     |
| `^addExchange`                                                            | `views.save_exchange`           | [save_exchange](finance-app-views.md#save-exchange)                     |
| `^removeExchange`                                                         | `views.remove_exchange`         | [remove_exchange](finance-app-views.md#remove-exchange)                 |
| `^getExchanges`                                                           | `views.get_exchanges`           | [get_exchanges](finance-app-views.md#get-exchanges)                     |
| `^cancelOrder`                                                            | `views.cancelOrder`             | [cancelOrder](finance-app-views.md#cancelorder)                         |
| `^statusaccount`                                                          | `views.account_status`          | [account_status](finance-app-views.md#account-status)                   |
| `^volume`                                                                 | `views.manage_volume`           | [manage_volume](finance-app-views.md#manage-volume)                     |
| `^testvolume`                                                             | `views.test_volume`             | [test_volume](finance-app-views.md#test-volume)                         |
| `^testAPI`                                                                | `views.testAPI`                 | [testAPI](finance-app-views.md#testapi)                                 |
| `^telegram/webhook`                                                       | `views.telegram_webhook`        | [telegram_webhook](finance-app-views.md#telegram-webhook)               |
