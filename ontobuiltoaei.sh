#!/bin/bash

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

buildind=$1

if [ $buildind = "True" ];
then
    docker build -t git.project-hobbit.eu:4567/jchakra1/ontoconn -f ./OntoSim/docker/oaei/Dockerfile ./OntoSim
elif [ $buildind = "False" ];
then
    echo "still figuring out how to test system in OAEI locally"
fi
