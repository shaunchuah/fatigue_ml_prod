#!/bin/bash

set -e

cd ~/fatigue_ml_prod/
echo "Begin app update..."
echo "Pulling from github..."
git pull || exit 1
echo "Activating python virtual environment..."
source ~/fatigue_ml_prod/venv/bin/activate
echo "Installing requirements.txt..."
pip install -r requirements.txt
echo "Completed app deployment."
