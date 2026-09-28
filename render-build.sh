#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update && apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip install -r requirements.txt