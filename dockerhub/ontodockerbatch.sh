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


chk_act_ind(){
    echo -e "\033[93m ------> Please Enter Source & Target OWL file path \033[0m"
    read onto_dir
    echo -e "\033[93m ------> Please Enter Source OWL file name \033[0m"
    read src_fl
    echo -e "\033[93m ------> Please Enter Target OWL file name \033[0m"
    read trgt_fl

    SRC_FILE=$onto_dir/$src_fl
    if [ -f $SRC_FILE ];
    then
        echo -e "\033[93m ------> source file is present \033[0m"
    else
        echo -e "\033[31m ------> source file is not present \033[0m"
        exit 1
    fi
    cp $onto_dir/$src_fl $onto_dir/"source.owl"

    TRGT_FILE=$onto_dir/$trgt_fl
    if [ -f $TRGT_FILE ];
    then
        echo -e "\033[93m ------> target file is present \033[0m"
    else
        echo -e "\033[31m ------> target file is not present \033[0m"
        exit 1
    fi
    cp $onto_dir/$trgt_fl $onto_dir/"target.owl"

    echo -e "\033[36m Output-rdf (with Timestamp) will be generated in the following path:- \033[0m"
    echo $onto_dir
}

if [ "$actind" = "start" ];
then
    chk_act_ind
    docker stop ontosim_app_batch
    docker rm ontosim_app_batch
    docker pull jchakra1/ontosim_imgbatch:v1
    docker run --name ontosim_app_batch -v $onto_dir:/usr/ontosim/java/ontofiles/local/ jchakra1/ontosim_imgbatch:v1
elif [ "$actind" = "stop" ];
then
    docker stop ontosim_app_batch
    docker rm ontosim_app_batch
elif [ "$actind" = "del" ];
then
    docker stop ontosim_app_batch
    docker rm ontosim_app_batch
    docker rmi -f $(docker images -q jchakra1/ontosim_imgbatch:v1)
fi
