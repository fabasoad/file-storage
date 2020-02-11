#!/bin/bash
cd /app-frontend
yarn install
yarn run build:prod
cd /app
pip3 install -r /app/requirements.txt
python3 -m src.rest