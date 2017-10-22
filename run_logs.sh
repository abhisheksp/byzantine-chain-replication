#!/usr/bin/env bash

source ~/Environments/async36/bin/activate
cd src
python -m da.compiler client.da
python -m da.compiler replica.da
python -m da.compiler olympus.da
python -m da.compiler main.da
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log  --message-buffer-size 100000 main.da -c single_client_workload.txt &
python -m da -n ClientNode --logfile --logfilename ../logs/client.log -D main.da &
