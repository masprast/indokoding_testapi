#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Collecting statics..."
python manage.py collectstatic
echo ====================================
