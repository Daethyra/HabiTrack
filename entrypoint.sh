#!/bin/sh

echo "Initializing database..."
flask db upgrade

echo "Starting Flask application..."
exec flask run --host=0.0.0.0
