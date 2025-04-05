# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**                                                             | **View Function**                              | **Function Documentation Link**                                              |
|-----------------------------------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------|
| `^getTelegram/$`                                                      | `userena_views.get_telegram`                   | [get_telegram](accounts-app-views.md#get-telegram)                           |
| `^newDeposit/$`                                                       | `userena_views.new_deposit`                    | [new_deposit](accounts-app-views.md#new-deposit)                             |
| `^getWallet/$`                                                        | `userena_views.get_wallet`                     | [get_wallet](accounts-app-views.md#get-wallet)                               |
| `^checkDeposits/$`                                                    | `userena_views.check_deposits`                 | [check_deposits](accounts-app-views.md#check-deposits)                       |
| `^getDeposits/$`                                                      | `userena_views.get_deposits`                   | [get_deposits](accounts-app-views.md#get-deposits)                           |
| `^signup/$`                                                           | `userena_views.signupsample`                   | [signupsample](accounts-app-views.md#signupsample)                           |
| `^settings/$`                                                         | `userena_views.settings`                       | [settings](accounts-app-views.md#settings)                                   |
| `^signup/$`                                                           | `userena_views.signup`                         | [signup](accounts-app-views.md#signup)                                       |
| `^signin/$`                                                           | `userena_views.signin`                         | [signin](accounts-app-views.md#signin)                                       |
| `^signout/$`                                                          | `userena_views.SignoutView`                    | [SignoutView](accounts-app-views.md#signoutview)                             |
| `^(?P<username>[\@\.\+\w-]+)/signup/complete/$`                       | `userena_views.direct_to_user_template`        | [direct_to_user_template](accounts-app-views.md#direct-to-user-template)     |
| `^activate/(?P<activation_key>\w+)/$`                                 | `userena_views.activate`                       | [activate](accounts-app-views.md#activate)                                   |
| `^activate/retry/(?P<activation_key>\w+)/$`                           | `userena_views.activate_retry`                 | [activate_retry](accounts-app-views.md#activate-retry)                       |
| `^(?P<username>[\@\.\+\w-]+)/pending/$`                               | `userena_views.activate_pending`               | [activate_pending](accounts-app-views.md#activate-pending)                   |
| `^(?P<username>[\@\.\+\w-]+)/email/$`                                 | `userena_views.email_change`                   | [email_change](accounts-app-views.md#email-change)                           |
| `^(?P<username>[\@\.\+\w-]+)/email/complete/$`                        | `userena_views.direct_to_user_template`        | [direct_to_user_template](accounts-app-views.md#direct-to-user-template)     |
| `^(?P<username>[\@\.\+\w-]+)/confirm-email/complete/$`                | `userena_views.direct_to_user_template`        | [direct_to_user_template](accounts-app-views.md#direct-to-user-template)     |
| `^confirm-email/(?P<confirmation_key>\w+)/$`                          | `userena_views.email_confirm`                  | [email_confirm](accounts-app-views.md#email-confirm)                         |
| `^(?P<username>[\@\.\+\w-]+)/disabled/$`                              | `userena_views.disabled_account`               | [disabled_account](accounts-app-views.md#disabled-account)                   |
| `^(?P<username>[\@\.\+\w-]+)/password/$`                              | `userena_views.password_change`                | [password_change](accounts-app-views.md#password-change)                     |
| `^(?P<username>[\@\.\+\w-]+)/password/complete/$`                     | `userena_views.direct_to_user_template`        | [direct_to_user_template](accounts-app-views.md#direct-to-user-template)     |
| `^(?P<username>[\@\.\+\w-]+)/edit/$`                                  | `userena_views.profile_edit`                   | [profile_edit](accounts-app-views.md#profile-edit)                           |
| `^(?P<username>(?!(signout\|signup\|signin)/)[\@\.\+\w-]+)/$`         | `userena_views.profile_detail`                 | [profile_detail](accounts-app-views.md#profile-detail)                       |
| `^page/(?P<page>[0-9]+)/$`                                            | `userena_views.ProfileListView.as_view`        | [ProfileListView](accounts-app-views.md#profilelistview)                     |
| `^$`                                                                  | `userena_views.ProfileListView.as_view`        | [ProfileListView](accounts-app-views.md#profilelistview)                     |

---
