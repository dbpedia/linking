#!/bin/bash

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

buildind=$1

echo -e "\033[93m ------> Please Enter Source & Target OWL file path \033[0m"
read onto_dir
echo -e "\033[93m ------> Please Enter Source OWL file name \033[0m"
read src_fl
cp $onto_dir/$src_fl $onto_dir/"source.owl"
echo -e "\033[93m ------> Please Enter Target OWL file name \033[0m"
read trgt_fl
cp $onto_dir/$trgt_fl $onto_dir/"target.owl"

echo -e "\033[36m Output-rdf (with Timestamp) will be generated in the following path:- \033[0m"
echo $onto_dir

if [ $buildind = "True" ];
then
    docker build -t ontosim_imgbatch:v1 -f ./OntoSim/docker/batch/Dockerfile ./OntoSim
    docker run --name ontosim_app_batch -v $onto_dir:/usr/ontosim/java/ontofiles/local/ ontosim_imgbatch:v1
elif [ $buildind = "False" ];
then
    docker stop ontosim_app_batch
    docker rm ontosim_app_batch
    docker run --name ontosim_app_batch -v $onto_dir:/usr/ontosim/java/ontofiles/local/ ontosim_imgbatch:v1
fi
