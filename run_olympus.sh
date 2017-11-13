#!/usr/bin/env bash

echo 'Deleting old log file: logs/olympus.log'
rm logs/olympus.log
echo 'Compiling DistAlgo files...'
source compile.sh
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n OlympusNode --logfile --logfilename ../logs/olympus.log --logfilelevel debug -D --message-buffer-size 100000 --hostname $IP_ADDR main.da
