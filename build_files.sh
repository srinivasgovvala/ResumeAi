#!/bin/bash
set -e

echo "Creating virtual environment..."
build_venv_dir="/tmp/resume-ai-build-venv"
python3 -m venv "$build_venv_dir"
source "$build_venv_dir/bin/activate"

echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Running Django commands..."
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_data
python manage.py configure_site
python manage.py configure_google_oauth
