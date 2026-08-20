#!/bin/bash
set -e

# Install dependencies (Vercel uses a managed environment, so we override the warning)
pip install -r requirements.txt --break-system-packages

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_data
python manage.py configure_site
python manage.py configure_google_oauth
