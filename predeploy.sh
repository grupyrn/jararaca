#!/bin/bash

npm run webpack
python manage.py collectstatic --noinput
django-admin compilemessages -f
