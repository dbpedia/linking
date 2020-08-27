#!/bin/bash

scriptflnm=$0
echo -e "\033[31;3m ${scriptflnm} is running \033[0m"

# Wait until Python Flask started and listens on port 5000.
while [ -z "`netstat -tln | grep 5000`" ]; do
echo 'Waiting for Python Flask to start ...'
sleep 1
done
echo 'Python Flask started.'

echo 'Starting java application...'
cd /usr/ontosim/java/
java -Xms6g -Xmx12g -cp /usr/ontosim/java/OntoSimilarity.jar org.hobbit.core.run.ComponentStarter com.ontosim.adapter.OntoConnAdapter

echo 'Closing python application'
supervisorctl stop pysim

echo 'Closing supervisor application'
kill -s SIGTERM $(supervisorctl pid)
