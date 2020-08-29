#!/bin/bash

## Arguments reference:
#$# -- number of args that our script was run with
#$0 -- the filename of our script
#$1..$n -- script arguments

echo ""
echo ""
echo -e '\033[32m ######################## OntoConnect System ######################## \033[0m'
echo ""
echo -e "\033[36m Please make sure the following requirements are maintained \033[0m"
echo -e "\033[36m 1) Atleast 15GB Harddisk \033[0m"
echo -e "\033[36m 2) Docker with atleast 10GB memory \033[0m"
echo ""
echo -e "\033[36m If the requirements do not meet, please exit the system \033[0m"
echo ""
echo -e "\033[32m #################################################################### \033[0m"
echo ""
echo ""

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

# Checking the environment
# prod/dev/test
envnm=$1
if [ -z "$envnm" ]
then
    echo -e '\033[31m ERROR: Environment is not set \033[0m'
    # Terminate our shell script with error
    exit 1
else
    echo -e "\033[31;3m Environment is  ${envnm} \033[0m"
fi

# Checking the activity
# start/stop/del
actnm=$2
if [ -z "$actnm" ]
then
    echo -e '\033[31m ERROR: Activity is not set \033[0m'
    # Terminate our shell script with error
    exit 1
else
    echo -e "\033[31;3m Activity is  ${actnm} \033[0m"
fi


# Checking the component-ind
# web/batch/oaei
COMP_IND="WEB"
chk_comp_ind(){
    echo -e "\033[93m --> What you want to run [WEB/BATCH/OAEI] ?  \033[0m"
    read comp_ind
    if [ "$comp_ind" == "batch" ] || [ "$comp_ind" == "BATCH" ];
    then
        COMP_IND="BATCH";
    elif [ "$comp_ind" == "oaei" ] || [ "$comp_ind" == "OAEI" ];
    then
        COMP_IND="OAEI";
    fi
}

if [ "$envnm" = "prod" ];
then
    #Calling chk_comp_ind function
    chk_comp_ind
    echo -e "\033[31;3m Choosen options are-  COMPONENT: ${COMP_IND} \033[0m"
    
    if [ $COMP_IND = "WEB" ];
    then
        ./ontodockerweb.sh $actnm
    elif [ $COMP_IND = "BATCH" ];
    then
        ./ontodockerbatch.sh $actnm
    elif [ $COMP_IND = "OAEI" ];
    then
        ./ontodockeroaei.sh $actnm
    fi
else
    echo "\033[31m ERROR: Environment is  not recognised \033[0m"
fi
