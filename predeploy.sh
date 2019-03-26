#!/bin/bash

echo "Packing React Check-in front end..."
yarn build

echo "Collecting static files..."
python manage.py collectstatic -i node_modules -i src -i package.json -i public -i scripts -i *.lock --noinput

echo "Compiling translations..."
django-admin compilemessages -f -v 0

echo "Applying migrations..."
python manage.py migrate

echo "Done."