#! /bin/bash -x

python cumplo/manage.py migrate 

python cumplo/manage.py runserver 0.0.0.0:8000