#!/bin/bash

# Start Nginx Web Server
service nginx start

cd /home/www/microblog                              # Go to project dir

if [ ! -f ./flaskenv/ ]; then
    python3 -m venv flaskenv
fi

source ./flaskenv/bin/activate                      # Activate Env for this project
./flaskenv/bin/pip install -r requirements.txt
./run.py                                            # Run Python Web Server
