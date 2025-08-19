#!/usr/bin/env bash
# exit on error
set -o errexit

# Clear pip cache to avoid conflicts
pip cache purge

# Install dependencies
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py populate_data
