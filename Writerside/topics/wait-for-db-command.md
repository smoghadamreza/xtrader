# Wait for DB
It is a general
[Django command](https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/)
defined in [](accounts-app.md) app.

## What does it do?
It waits for all db connections to be up and running and then
finishes.

## When does it run?
  In ```run.sh``` file which is the entrypoint for starting the project.   #TODO: add reference.
  
## Where is it?

```
  xtrader/
  │── accounts/
  │   ├── management/
  │   │   ├── commands/
  │   │   │   ├── wait_for_db.py
```

## How to run it? 
Like all customized django commands as follows:
```bash
python manage.py wait_for_db
```
