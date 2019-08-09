#!/bin/bash

## Arguments reference:
#$# -- number of args that our script was run with
#$0 -- the filename of our script
#$1..$n -- script arguments

DEV="dev"
PROD="prod"

BASE_DIR=""

scriptflnm=$0
echo "${scriptflnm} is running"

envnm=$1
if [ "$envnm" = $DEV ]
then
    echo "Please Enter Base Directory"
    read local_base_dir
    BASE_DIR=$local_base_dir
elif [ "$envnm" = $PROD ]
then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    echo "current directory is ${DIR}"
    BASE_DIR=$DIR"/linking_python/OntoSimPY"
    MODEL_DIR=$DIR"/linking_python/py_model"
else
    echo "Environment is  not recognised"
fi

if [ ! -z "$BASE_DIR" ]
then
    #Creating Data Folder
    echo "Creating folder in ${BASE_DIR}"
    mkdir -m 777 -p $BASE_DIR"/ontodata/eclipse"
    mkdir -m 777 -p $BASE_DIR"/ontodata/output"
    mkdir -m 777 -p $BASE_DIR"/ontodata/output/word_sim"
    mkdir -m 777 -p $BASE_DIR"/ontodata/modifylbl"
    mkdir -m 777 -p $BASE_DIR"/ontodata/dict"
    mkdir -m 777 -p $BASE_DIR"/ontodata/fastentity"
    mkdir -m 777 -p $BASE_DIR"/ontodata/entityvec"
    mkdir -m 777 -p $BASE_DIR"/ontodata/finalentity/300"
    mkdir -m 777 -p $BASE_DIR"/ontodata/loss/ontomodify"
    mkdir -m 777 -p $BASE_DIR"/ontodata/train_test_tree"
    mkdir -m 777 -p $BASE_DIR"/ontodata/util"
    mkdir -m 777 -p $BASE_DIR"/ontodata/util/graph"
    echo "Creating folder in ${MODEL_DIR}"
    mkdir -m 777 -p $MODEL_DIR"/model/onto_model"
    mkdir -m 777 -p $MODEL_DIR"/model/fasttext"

    echo "----> Do you want to copy FastText pretrained model[Y/N]"
    read copy_ind
    if [ "$copy_ind" == "Y" ] || [ "$copy_ind" == "y" ];
    then
        echo "------> Please Enter FastText pretrained model"
        read fast_txt_dir
        cp $fast_txt_dir $MODEL_DIR"/model/fasttext"
    fi


    echo "----> Do you want to copy OntoModel pretrained model[Y/N]"
    read copy_ind
    if [ "$copy_ind" == "Y" ] || [ "$copy_ind" == "y" ];
    then
        echo "------> Please Enter OntoModel pretrained model"
        read onto_model_dir
        cp $onto_model_dir $MODEL_DIR"/model/onto_model"
    fi

fi

