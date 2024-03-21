#! /usr/bin/env bash

# change to python virtual environment(venv)
source .venv/Scripts/activate

# use source ./start.sh as it has export below
export PYTHONPATH=$PWD

# Let the DB start
cd app
python backend_pre_start.py
cd ..

# Run migrations
alembic upgrade head

# Create initial data in DB
cd app
python initial_data.py
cd ..