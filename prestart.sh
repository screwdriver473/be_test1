#! /usr/bin/env bash

#none: 0, mac: 1, ubuntu: 2, windows: 3
os_platform=0

is_script_sourced() {
	#check if your bash supports BASH_SOURCE variable
	# man bash | less -p BASH_SOURCE
	[[ ${BASH_VERSINFO[0]} -le 2 ]] && echo 'No BASH_SOURCE array variable' && echo "Hope you are sourcing this script!"

	if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
		echo "script ${BASH_SOURCE[0]} is being sourced ..."
	else
		echo "script ${BASH_SOURCE[0]} is NOT being sourced ..."
		exit 2
	fi
}

is_script_sourced

if [[ $os_platform -eq 0 ]]; then
	if [[ $OSTYPE == "darwin"* ]]; then
		echo '---> macOS'
		os_platform=1
	elif [[ $OSTYPE == "linux"* ]]; then
		echo '---> linux/ubuntu OS'
		os_platform=2
	elif [[ $OSTYPE == "mysys" ]]; then
		echo '---> windows/vs'
		os_platform=3
	else
		echo "Unknown OS platform..."
		exit 3
	fi
fi

# change to python virtual environment(venv)
if [[ $os_platform -eq 1 ]]  || [[ $os_platform -eq 2 ]]; then
	#for Linux/Mac
	source .venv/bin/activate
elif [[ $os_platform -eq 3 ]]; then
	#for Windows
	source .venv/Scripts/activate
else
	echo "Python virtual env create failed.."
	exit 4
fi

if [ ! -f .pkg_init_done ]; then
	if [[ $os_platform -eq 3 ]]; then
		#Windows
		python3 -m pip install -r requirements.txt
	else
		#Mac
		python3 -m pip install -r requirements_mac.txt
	fi
	if [ $? -eq 0 ]; then
		touch .pkg_init_done
	else
		echo "---------> Some error while installing python packages!"
		exit 1
	fi
else
	echo "Seems packages init is already done, moving ahead!!"
fi

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
