#!/bin/bash

## Arguments reference:
#$# -- number of args that our script was run with
#$0 -- the filename of our script
#$1..$n -- script arguments

DEV="dev"
TEST="test"
PROD="prod"

START="start"
STOP="stop"
DEL="del"

scriptflnm=$0
echo "${scriptflnm} is running"

envnm=$1
if [ -z "$envnm" ]
then
    echo -e '\033[31m ERROR: Environment is not set \033[0m'
    exit 1
else
    echo "Environment is  ${envnm}"
fi

actnm=$2
if [ -z "$actnm" ]
then
    echo -e '\033[31m ERROR: Activity is not set \033[0m'
    exit 1
else
    echo "Activity is  ${actnm}"
fi

if [ "$envnm" = $DEV ] && [ "$actnm" = $START ]
then
    docker-compose -f docker-compose-dev.yml up --build
elif [ "$envnm" = $TEST ] && [ "$actnm" = $START ]
then
    docker-compose -f docker-compose-test.yml up --build
elif [ "$envnm" = $PROD ] && [ "$actnm" = $START ]
then
    docker-compose -f docker-compose-prod.yml up --build
elif [  "$envnm" = $DEV ] && [ "$actnm" = $STOP ]
then
    docker-compose -f docker-compose-dev.yml down
    docker image prune #Remove unused images
elif [  "$envnm" = $TEST ] && [ "$actnm" = $STOP ]
then
    docker-compose -f docker-compose-test.yml down
    docker image prune #Remove unused images
elif [  "$envnm" = $PROD ] && [ "$actnm" = $STOP ]
then
    docker-compose -f docker-compose-prod.yml down
    docker image prune #Remove unused images
elif [ "$actnm" = $DEL ]
then
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)
else
    echo "Environment or Activity is  not recognised"
fi
