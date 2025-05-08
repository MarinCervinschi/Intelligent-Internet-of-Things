#!/bin/zsh
#File run.sh

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .flaskenv.example .flaskenv

flask run
