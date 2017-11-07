#!/usr/bin/env bash

source compile.sh
rm logs/olympus.log
cd src
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n OlympusNode --logfile --logfilename ../logs/olympus.log --logfilelevel debug -D --message-buffer-size 100000 --hostname $IP_ADDR main.da
