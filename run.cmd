#!/bin/bash

# Start Nginx Web Server
service nginx start

cd /home/www/microblog              # Go to project dir
source ./flaskenv/bin/activate      # Activate Env for this project
./run.py                            # Run Python Web Server
