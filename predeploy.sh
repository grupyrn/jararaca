#!/bin/bash

echo "Packing React Check-in front end..."
npm run webpack

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Compiling translations..."
django-admin compilemessages -f -v 0

echo "Applying migrations..."
python manage.py migrate

echo "Done."