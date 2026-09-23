#!/usr/bin/env bash
# Start the Flask backend
cd "$(dirname "$0")/backend"
pip install -r requirements.txt
python app.py
