# xtrader 

## Generate ERD

First create a conda envrionment named `xtrader-env` by what is instructed in the `Dockerfile`. Then run the following command:

`conda run -n xtrader-env python manage.py graph_models -a -g -o ../Writerside/images/ERD.png`


## Run Migration

Run this at the root of the project (where `docker-compose.yml` resides):
1) `docker-compose build --no-cache`
2) `docker-compose run --rm --no-deps --entrypoint "" app conda run -n xtrader-env python manage.py makemigrations`
3) `docker-compose run --rm --no-deps --entrypoint "" app conda run -n xtrader-env python manage.py migrate`

⚠️ HEADS UP!
You might need to run `docker-compose` command with `sudo` priviledges.


## Run Local

1) `docker-compose down -v --remove-orphans`
2) `docker-compose build --no-cache`
3) `docker-compose up -d`

To check container logs: 
`docker-compose logs -f app`

Find the project on browser: 
Address: `http://localhost:8000`

