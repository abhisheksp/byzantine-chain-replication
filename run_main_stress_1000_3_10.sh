#!/usr/bin/env bash

source ~/Environments/async36/bin/activate
rm logs/main.log
cd src
python -m da.compiler client.da
python -m da.compiler replica.da
python -m da.compiler olympus.da
python -m da.compiler main.da
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log --logfilelevel info --message-buffer-size 1000000 main.da -c stress_100.txt