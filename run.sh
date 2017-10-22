#!/usr/bin/env bash

source ~/Environments/async36/bin/activate
cd src
python -m da client.da
python -m da replica.da
python -m da olympus.da
python -m da main.da
python -m da -n MainNode --master  --message-buffer-size 1000000 main.da