#!/bin/bash

## Arguments reference:
#$# -- number of args that our script was run with
#$0 -- the filename of our script
#$1..$n -- script arguments

DEV="dev"
PROD="prod"

BASE_DIR=""

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

envnm=$1
compind=$2

if [ "$envnm" = $PROD ]
then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    echo -e "\033[31;3m current directory is \033[0m"
    echo "-: ${DIR}"
    PY_BASE_DIR=$DIR"/OntoSim/linking_python/OntoSimPY"
    JAVA_BASE_DIR=$DIR"/OntoSim/linking_java"
    MODEL_DIR=$DIR"/OntoSim/linking_python/py_model"
else
    echo "\033[31m Environment is  not recognised \033[0m"
fi

if [ ! -z "$PY_BASE_DIR" ]
then
    #Creating Data Folder
    echo -e "\033[31;3m Creating java-folder in \033[0m"
    echo "-: ${JAVA_BASE_DIR}"
    mkdir -m 777 -p $JAVA_BASE_DIR"/ontofiles/local/"
    mkdir -m 777 -p $JAVA_BASE_DIR"/ontofiles/oaei/"
    echo -e "\033[31;3m Creating python-folder in \033[0m"
    echo "-: ${PY_BASE_DIR}"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/eclipse"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/output"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/output/word_sim"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/modifylbl"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/dict"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/fastentity"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/entityvec"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/finalentity/300"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/loss/ontomodify"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/train_test_tree"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/util"
    mkdir -m 777 -p $PY_BASE_DIR"/ontodata/util/graph"
    echo -e "\033[31;3m Checking python-model in \033[0m"
    echo ":- ${MODEL_DIR}"
    FASTTEXT_FILE=$MODEL_DIR"/model/fasttext/fast.bin"

    echo -e "\033[34m >> $FASTTEXT_FILE \033[0m"
    if [ -f $FASTTEXT_FILE ];
    then
        echo -e "\033[93m ------> FastText pretrained model is present \033[0m"
    else
        echo -e "\033[31m ------> FastText pretrained model is not present \033[0m"
        echo "Please copy FastText pretrained model (fast.bin) in the below location"
        echo ":- ${MODEL_DIR}/model/fasttext/"
        exit 1
    fi


    echo -e "\033[93m ----> Please check whether correct OntoModel pretrained model is present or not \033[0m"
    echo -e "\033[93m ----> Below is the list of model present: \033[0m"
    for entry in "${MODEL_DIR}/model/onto_model"/*
    do
        echo -e "\033[34m >> $entry \033[0m"
    done
    echo -e "\033[93m ----> If OntoModel pretrained model is not present, Please copy in the below location \033[0m"
    echo ":- ${MODEL_DIR}/model/onto_model/"

fi

