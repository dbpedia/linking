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