#!/usr/bin/env bash

source ~/Environments/async36/bin/activate
rm logs/client.log
cd src
python -m da.compiler client.da
python -m da.compiler replica.da
python -m da.compiler olympus.da
python -m da.compiler main.da
python -m da -n ClientNode --logfile --logfilename ../logs/client.log --logfilelevel info -D --message-buffer-size 100000 main.da
