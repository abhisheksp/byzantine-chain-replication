#!/usr/bin/env bash

source clean_containers.sh
source compile.sh
rm logs/main.log
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n MainNode --logfile --logfilename ../logs/main.log --logfilelevel debug --message-buffer-size 100000 --hostname $IP_ADDR main.da -c single_client_workload.txt