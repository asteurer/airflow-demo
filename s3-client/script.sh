#!/bin/bash

set -a
source .env
set +a

python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

spin up --build --listen 0.0.0.0:3000
