#!/bin/bash

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

actind=$1
if [ -z "$actind" ]
then
    echo -e '\033[31m ERROR: Activity is not set \033[0m'
    exit 1
else
    echo -e "\033[31;3m Activity is ${actind} \033[0m"
fi

if [ "$actind" = "start" ];
then
    docker stop ontosim_app_web
    docker rm ontosim_app_web
    docker pull jchakra1/ontosim_imgweb:v1
    docker run --name ontosim_app_web -p 8080:8080 jchakra1/ontosim_imgweb:v1
elif [ "$actind" = "stop" ];
then
    docker stop ontosim_app_web
    docker rm ontosim_app_web
elif [ "$actind" = "del" ];
then
    docker stop ontosim_app_web
    docker rm ontosim_app_web
    docker rmi -f $(docker images -q jchakra1/ontosim_imgweb:v1)
fi
