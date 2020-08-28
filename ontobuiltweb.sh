#!/bin/bash

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

buildind=$1

if [ $buildind = "True" ];
then
    docker build -t ontosim_imgweb:v1 -f ./OntoSim/docker/web/Dockerfile ./OntoSim
    docker run -p 8080:8080 --name ontosim_app_web ontosim_imgweb:v1
elif [ $buildind = "False" ];
then
    docker stop ontosim_app_web
    docker rm ontosim_app_web
    docker run -p 8080:8080 --name ontosim_app_web ontosim_imgweb:v1
fi
