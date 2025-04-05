# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**                                 | **View Function**                          | **Function Documentation Link**                                  |
|-------------------------------------------|--------------------------------------------|------------------------------------------------------------------|
| `^$`                                      | `views.management`                         | [management](aum-app-views.md#management)                        |
| `^issueOrRedeemUnit`                      | `views.issue_redeem_unit`                  | [issue_redeem_unit](aum-app-views.md#issue-redeem-unit)          |
| `^redeemUnit`                             | `views.redeem_unit`                        | [redeem_unit](aum-app-views.md#redeem-unit)                      |
| `^addInvestor`                            | `views.add_investor`                       | [add_investor](aum-app-views.md#add-investor)                    |
| `^transactionsHistory`                    | `views.transactions_history`               | [transactions_history](aum-app-views.md#transactions-history)    |
| `^investors`                              | `views.investors`                          | [investors](aum-app-views.md#investors)                          |
| `^getFund`                                | `views.get_fund`                           | [get_fund](aum-app-views.md#get-fund)                            |
| `^initFundPerformance`                    | `views.init_fund_performance`              | [init_fund_performance](aum-app-views.md#init-fund-performance)  |
| `^fundPerformance`                        | `views.get_fund_performance`               | [get_fund_performance](aum-app-views.md#get-fund-performance)    |
