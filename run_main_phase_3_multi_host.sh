#!/usr/bin/env bash

echo 'Cleaning Existing Replica Containers...'
source clean_containers_images.sh
echo 'Building new Replica Image'
docker build -t replicanode_img .
echo 'Deleting old log file: logs/main.log'
rm logs/main.log
echo 'Deleting old log file: logs/replica.log'
rm logs/replica.log
echo 'Deleting old persisted states'
rm logs/replica_state_*
rm logs/client_state_*
echo 'Compiling DistAlgo files...'
source compile.sh
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n MainNode --logfile --logfilename ../logs/main.log --logfilelevel info --message-buffer-size 100000 --hostname $IP_ADDR main.da -c perform900_multi.txt