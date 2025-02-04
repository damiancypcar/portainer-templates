#!/usr/bin/env bash

activate-venv() {
if [ ! -d "venv" ]; then
    echo "  - missing \"venv\", createing..."
    python -m venv venv
fi

if [ -d "venv" ]; then
    echo "  - activating \"venv\""

    if [ -n "$WINDIR" ]; then
        # Windows
        .\venv\Scripts\activate
    else
        # Unix/Linux/macOS
        source venv/bin/activate
    fi
fi
}

echo -e "\u2023 Activate venv"
activate-venv

echo -e "\u2023 Install dependencies"
python -m pip -V
# python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt

echo -e "\u2023 Run python script"
python build-templates.py


echo "End"
