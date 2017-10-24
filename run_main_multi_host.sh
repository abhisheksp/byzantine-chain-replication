#!/usr/bin/env bash

source compile.sh
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log --logfilelevel info --hostname <IP> --message-buffer-size 100000 main.da -c single_client_workload.txt