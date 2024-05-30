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

# use source ./start.sh as it has export below
export PYTHONPATH=$PWD
cd app
uvicorn main:app

cd -

# come out of python venv
#deactivate
