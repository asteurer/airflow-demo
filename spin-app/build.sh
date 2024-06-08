#!/bin/bash

set -a
source ../../lambda_migration/.env
set +a

# python -m virtualenv venv
# source venv/bin/activate

# pip install -r requirements.txt

# spin up --build

spin up --listen 0.0.0.0:3000