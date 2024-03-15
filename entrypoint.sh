#!/bin/bash


python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py populate_database


gunicorn backend.wsgi:application --bind=0.0.0.0:8000 --reload