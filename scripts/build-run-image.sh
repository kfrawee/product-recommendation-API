#!/bin/bash
# Build the Docker image
docker build -t genify-api .

# Run the Docker container in the background
docker run -d -p 8080:8080 genify-api 

