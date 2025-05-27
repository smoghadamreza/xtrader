# xtrader 

## Generate ERD

First create a conda envrionment named `xtrader-env` by what is instructed in the `Dockerfile`. Then run the following command:

`conda run -n xtrader-env python manage.py graph_models -a -g -o ../Writerside/images/ERD.png`
