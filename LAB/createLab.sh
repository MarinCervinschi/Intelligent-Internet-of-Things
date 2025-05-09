#!/bin/sh
#File createLab.sh


if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <lab_name>"
    exit 1
fi

lab_name=$1

echo "Creating directory: $lab_name"
mkdir -p "$lab_name"

cd "$lab_name"

if [ $? -ne 0 ]; then
    echo "Failed to create or change to directory $lab_name"
    exit 1
fi

echo "Creating Python virtual environment in $lab_name/.venv"
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    exit 1
fi

echo "Activating the virtual environment"
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

echo "Setup complete. Virtual environment is ready."

open -a "Visual Studio Code" .
if [ $? -ne 0 ]; then
    echo "Failed to open Visual Studio Code"
    exit 1
fi
echo "Visual Studio Code opened in $lab_name directory."
