#!/bin/bash

# Check if Flask server is running
if ! curl -sSf "http://localhost:8080/"; then
  echo "Flask server is not running. Please start it first"
  exit 1
fi

# Check if admin user is created
response=$(curl -sSf -X POST \
  http://localhost:8080/api/v1/security/login \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"username": "admin" ,"password": "admin", "provider": "db"}')
if [[ $response == *"Unauthorized"* ]]; then
  echo "Admin user is not created"
  # Create admin user
  export FLASK_APP=app
  flask fab create-admin
fi

# Use admin user to login
curl -X POST \
  http://localhost:8080/api/v1/security/login \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"username": "admin" ,"password": "admin", "provider": "db"}'
