#!/usr/bin/env bash

source compile.sh
rm logs/client.log
export IP_ADDR=`/sbin/ifconfig docker0 |grep 'inet '| cut -d: -f2 | awk '{print $2}'`
python -m da -n ClientNode --logfile --logfilename ../logs/client.log --logfilelevel debug -D --message-buffer-size 100000 --hostname $IP_ADDR main.da
