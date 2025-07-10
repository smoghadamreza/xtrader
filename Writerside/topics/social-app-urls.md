# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**                              | **View Function**              | **Function Documentation Link**                          |
|----------------------------------------|--------------------------------|----------------------------------------------------------|
| `^exchange`                            | `views.exchange`               | [exchange](social-app-views.md#exchange)                 |
| `^protraders`                          | `views.protraders`             | [protraders](social-app-views.md#protraders)             |
| `^copytrading`                         | `views.copytrading`            | [copytrading](social-app-views.md#copytrading)           |
| `^copytrade`                           | `views.follow_unfollow`        | [follow_unfollow](social-app-views.md#follow-unfollow)   |
| `^copyorder`                           | `views.copy_order`             | [copy_order](social-app-views.md#copy-order)             |
| `^getpublics`                          | `views.getpublics`             | [getpublics](social-app-views.md#getpublics)             |
| `^promote`                             | `views.promote`                | [promote](social-app-views.md#promote)                   |
| `^trader`                              | `views.trader`                 | [trader](social-app-views.md#trader)                     |
| `^getProfile/(?P<pro_id>\w+)`          | `views.get_profile`            | [get_profile](social-app-views.md#get-profile)           |
| `^league`                              | `views.league`                 | [league](social-app-views.md#league)                     |
