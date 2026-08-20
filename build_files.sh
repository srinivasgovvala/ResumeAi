#!/bin/bash
set -e
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_data
python manage.py configure_site
python manage.py configure_google_oauth
