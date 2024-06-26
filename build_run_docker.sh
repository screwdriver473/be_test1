#!/bin/bash

img_tag="v1.0.0"
img_name="backend"
backend_inst_port=8000
container_name="backend_instance1"
postgres_port=5438 #$(grep POSTGRES_PORT app/.env | awk -F= '{print $2}')
dont_use_cache=1

if [[ -f Dockerfile ]]; then
    rm -rf .venv
    if [[ $dont_use_cache -eq 1 ]]; then
        docker build . --no-cache -t $img_name:$img_tag
    else
        docker build . -t $img_name:$img_tag
    fi
    #docker image ls
    ##docker run --name $container_name --rm -p $backend_inst_port:$backend_inst_port -p $postgres_port:$postgres_port $img_name:$img_tag
    #docker container ls
    #docker ps -a
    
else
    echo "Dockerfile not found"
fi