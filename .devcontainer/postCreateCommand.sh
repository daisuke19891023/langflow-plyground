#!/bin/sh
# postCreateCommand.sh

echo "START Install"

sudo chown -R vscode:vscode .
poetry config virtualenvs.in-project true
poetry install

# to install webscraping tools
playwright install
playwright install-deps

# activate vertual env
source .venv/bin/activate
echo "FINISH Install"