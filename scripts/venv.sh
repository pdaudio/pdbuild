#!/bin/bash

# abort on errors
set -e

# check for first parameter, the path where to create the virtual environment
if [ "$#" -ne 1 ]; then
    echo "Invalid argument count. Please give exactly one parameter where to create the virtual build environment."
fi

# check path of virtual environment, remove if already present
VENV_ROOT=$( readlink -f "$1" )
VENV_DIR="$VENV_ROOT/.venv"
if [ -e "$VENV_DIR" ]; then
    if ! [ -d "$VENV_DIR" ]; then
        echo "can not create virtual environment in $VENV_DIR - file exists but is not a directory"
    else
        rm -rf "$VENV_DIR"
    fi
fi

# go to pdbootstrap directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PDBUILD_ROOT=$(dirname "$SCRIPT_DIR")
PDBOOTSTRAP_DIR="$PDBUILD_ROOT/pdbootstrap"
cd "$PDBOOTSTRAP_DIR"

# build pdbootstrap
$SCRIPT_DIR/build.sh

# build virtual python environment
echo "building virtual python environment in $VENV_DIR"
cd "$VENV_ROOT"
python3 -m venv "$VENV_DIR"

# install pdbootstrap package into virtual environment
"$VENV_DIR/bin/python3" -m pip install $PDBOOTSTRAP_DIR/dist/*.tar.gz

# show informations
echo "To run in the virtual environment add it to the PATH variable by executing:"
echo "export PATH=\"$VENV_DIR/bin:\$PATH\""
