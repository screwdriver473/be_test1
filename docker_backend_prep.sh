#! /usr/bin/env bash

#if [ ! -f .pkg_init_done ]; then
#	#python3 -m pip install -r requirements.txt
#	pip install --no-cache-dir --upgrade -r requirements.txt
#	if [ $? -eq 0 ]; then
#		touch .pkg_init_done
#	else
#		echo "---------> Some error while installing python packages!"
#		exit 1
#	fi
#else
#	echo "Seems packages init is already done, moving ahead!!"
#fi

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

echo "$@ =======>> execution done......!!"
