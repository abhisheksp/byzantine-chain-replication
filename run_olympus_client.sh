#!/usr/bin/env bash

source kill_processes.sh
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
echo 'Cleaning Existing Replica Containers...'
source clean_containers_images.sh
echo 'Building new Replica Image'
docker build -t replicanode_img .
echo 'Deleting old log file: logs/main.log'
rm logs/main.log
echo 'Deleting old log file: logs/olympus.log'
rm logs/olympus.log
echo 'Deleting old log file: logs/client.log'
rm logs/client.log
echo 'Compiling DistAlgo files...'
source compile.sh
python -m da -n ClientNode --logfile --logfilename ../logs/client.log --logfilelevel debug -D --message-buffer-size 100000 --hostname $IP_ADDR main.da > /dev/null 2>&1 &
python -m da -n OlympusNode --logfile --logfilename ../logs/olympus.log --logfilelevel debug -D --message-buffer-size 100000 --hostname $IP_ADDR main.da > /dev/null 2>&1 &
python -m da -n MainNode --logfile --logfilename ../logs/main.log --logfilelevel debug --message-buffer-size 100000 --hostname $IP_ADDR main.da -c single_client_workload.txt > /dev/null 2>&1 &