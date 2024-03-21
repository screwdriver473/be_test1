#! /usr/bin/env bash

# change to python virtual environment(venv)
source .venv/Scripts/activate

# use source ./start.sh as it has export below
export PYTHONPATH=$PWD
cd app
uvicorn main:app

cd -

# come out of python venv
#deactivate