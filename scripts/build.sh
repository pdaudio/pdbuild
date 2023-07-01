#!/bin/bash

# abort on errors
set -e

# go to pdbootstrap directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PDBUILD_ROOT=$(dirname "$SCRIPT_DIR")
PDBOOTSTRAP_DIR="$PDBUILD_ROOT/pdbootstrap"
cd "$PDBOOTSTRAP_DIR"

# remove last build directory
if [ -d ./dist ]; then
    rm -rf ./dist
fi
if [ -d ./pdbootstrap.egg-info ]; then
    rm -rf ./pdbootstrap.egg-info
fi

# upgrade python build system
python3 -m pip install --upgrade build

# build pdbootstrap
python3 -m build
