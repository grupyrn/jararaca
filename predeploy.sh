#!/bin/bash

# Pre-deploy script
# Note: Build steps (yarn, collectstatic, compilemessages) are now handled in the Dockerfile.
# This script runs on the deployed container to apply database changes.

echo "Applying migrations..."
python manage.py migrate

echo "Done."
