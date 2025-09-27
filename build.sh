#!/bin/bash

# Exit on error
set -o errexit


# Collect static files
python manage.py collectstatic --no-input