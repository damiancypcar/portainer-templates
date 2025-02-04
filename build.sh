#!/usr/bin/env bash

activate-venv() {
if [ ! -d "venv" ]; then
    echo "  - missing \"venv\", createing..."
    python -m venv venv
fi

if [ -d "venv" ]; then
    echo "  - activating \"venv\""
    source ./venv/Scripts/activate

fi
}

echo -e "\u2023 Activate venv"
activate-venv

echo -e "\u2023 Install dependencies"
# python -m pip -V
# python -m pip install pyyaml ruamel.yaml
# python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt

echo -e "\u2023 Run python script"
python build-templates2.py




echo "koniec"
