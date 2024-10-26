#!/bin/sh

sudo apt update
sudo apt install -y vim iputils-ping

echo "create virtual environment"
python3 -m venv .venv

echo "activate virtual environment" 
source .venv/bin/activate

echo "install requirements"
pip3 install -r requirements.txt