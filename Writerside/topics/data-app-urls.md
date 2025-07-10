# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**                                               | **View Function**                  | **Function Documentation Link**                          |
|---------------------------------------------------------|------------------------------------|----------------------------------------------------------|
| `^symbols`                                              | `views.get_symbols`                | [get_symbols](data-app-views.md#get-symbols)             |
| `^allSymbols`                                           | `views.get_all_symbols`            | [get_all_symbols](data-app-views.md#get-all-symbols)     |
| `^intervals/$`                                          | `views.get_intervals`              | [get_intervals](data-app-views.md#get-intervals)         |
| `^history/$`                                            | `views.history`                    | [history](data-app-views.md#history)                     |
| `^stockwatch/(?P<SymbolId>\w+)/$`                       | `views.stockwatch`                 | [stockwatch](data-app-views.md#stockwatch)               |
| `^symbol-search/q=(?P<query>\w+)`                       | `views.symbol_search`              | [symbol_search](data-app-views.md#symbol-search)         |
| `^get-data/(?P<symbol_id>\w+)/(?P<interval>\w+)`        | `views.get_data`                   | [get_data](data-app-views.md#get-data)                   |
