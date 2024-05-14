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
# it generates a file in app/alembic/versions
alembic revision --autogenerate -m "added patient tables"
alembic upgrade head

# Create initial data in DB
cd app
python initial_data.py
cd ..