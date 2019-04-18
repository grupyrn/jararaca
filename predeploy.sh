#!/bin/bash

echo "Running yarn"
yarn

echo "Packing React Check-in front end..."
yarn build

echo "Collecting static files..."
python manage.py collectstatic -i node_modules -i src -i package.json -i public -i scripts -i *.lock --noinput

echo "Compiling translations..."
django-admin compilemessages -f -v 0

echo "Applying migrations..."
python manage.py migrate

echo "Removing Node packages..."
find -type d -name "node_modules" -printf "%p\n"|sort -nr | xargs rm -rf

echo "Done."
