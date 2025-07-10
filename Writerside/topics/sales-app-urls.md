# URLs

Django framework offers some functions which we can use to create a tree like structure for our 
website links. In this way every node's link will be appended to the link of its parent. We store these 
(local) links in files named `urls.py`. For more information on the subject visit this 
<include from="repeatable-texts.topic" element-id="django-urls"/>.

## URL List

| **Route**               | **View Function**          | **Function Documentation Link**                  |
|-------------------------|----------------------------|--------------------------------------------------|
| `^packages/$`           | `views.get_packages`       | [get_packages](sales-app-views.md#get-packages)  |
| `^subscribe/$`          | `views.subscribe`          | [subscribe](sales-app-views.md#subscribe)        |
