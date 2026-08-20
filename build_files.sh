#!/bin/bash
set -e

echo "Creating virtual environment..."
python3 -m venv .vercel-venv
source .vercel-venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Running Django commands..."
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_data
python manage.py configure_site
python manage.py configure_google_oauth
