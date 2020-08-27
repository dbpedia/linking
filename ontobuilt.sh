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


# Checking the build-ind
# true/false
BUILD_NEEDED="False"
chk_build_ind(){
    echo -e "\033[93m --> Do you want to build from scratch [Y/N] ? \033[0m"
    read build_ind
    if [ "$build_ind" == "Y" ] || [ "$build_ind" == "y" ];
    then
        BUILD_NEEDED="True";
    fi
}


# Checking the component-ind
# web/batch/oaei
COMP_IND="WEB"
chk_comp_ind(){
    echo -e "\033[93m --> What you want to build [WEB/BATCH/OAEI] ?  \033[0m"
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
    if [ "$actnm" = "start" ];
    then
        #Calling chk_build_ind function
        chk_build_ind
        #Calling chk_comp_ind function
        chk_comp_ind
        echo -e "\033[31;3m Choosen options are-  BUILD: ${BUILD_NEEDED}  COMPONENT: ${COMP_IND} \033[0m"
        ./ontodrivecrt.sh $envnm $COMP_IND
        if [ $COMP_IND = "WEB" ];
        then
            ./ontobuiltweb.sh $BUILD_NEEDED
        elif [ $COMP_IND = "BATCH" ];
        then
            ./ontobuiltbatch.sh $BUILD_NEEDED
        elif [ $COMP_IND = "OAEI" ];
        then
            ./ontobuiltoaei.sh $BUILD_NEEDED
        fi
    elif [ "$actnm" = "stop" ];
    then
        docker stop ontosim_app_web
	docker stop ontosim_app_batch
    elif [ "$actnm" = "del" ];
    then
        docker rmi -f $(docker images -q ontosim_imgweb:v1)
        docker rmi -f $(docker images -q ontosim_imgbatch:v1)
        docker rmi -f $(docker images -q git.project-hobbit.eu:4567/jchakra1/ontoconn:latest)
        
        docker stop ontosim_app_web
        docker rm ontosim_app_web
        docker stop ontosim_app_batch
        docker rm ontosim_app_batch

        #docker rmi -f $(docker images -f "dangling=true" -q)
        #docker system prune
    else
        echo "\033[31m ERROR: Activity is  not recognised \033[0m"
    fi
else
    echo "\033[31m ERROR: Environment is  not recognised \033[0m"
fi
