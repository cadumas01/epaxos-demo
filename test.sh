#!/bin/sh

timeout 180s bin/client -maddr=10.182.0.21 -writes=$1 -c=$2 -T=$3
python3 client_metrics.py


