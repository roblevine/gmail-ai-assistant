#!/bin/sh
echo "starting installation script"

echo "update and install apt packages"
sudo apt update
sudo apt upgrade -y
sudo apt install -y vim iputils-ping dos2unix

echo "create virtual environment"
python3 -m venv .venv

echo "activate virtual environment" 
source .venv/bin/activate

echo "upgrade pip"
python -m pip install -U pip

echo "install requirements"
pip install -r requirements.txt

echo "installation script complete"