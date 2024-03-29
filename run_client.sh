#!/usr/bin/env bash

echo 'Deleting old log file: logs/client.log'
rm logs/client.log
echo 'Compiling DistAlgo files...'
source compile.sh
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n ClientNode --logfile --logfilename ../logs/client.log --logfilelevel info -D --message-buffer-size 100000 --hostname $IP_ADDR main.da
