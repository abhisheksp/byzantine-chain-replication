#!/usr/bin/env bash

source ~/Environments/async36/bin/activate
cd src
python -m da.compiler client.da
python -m da.compiler replica.da
python -m da.compiler olympus.da
python -m da.compiler main.da
python -m da -n MainNode --master  --message-buffer-size 1000000 main.da -c single_client_workload.txt