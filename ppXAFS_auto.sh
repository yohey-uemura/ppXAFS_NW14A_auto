#! /bin/bash
export PATHTOLARCH=$HOME/xraylarch   ####set path to xraylarch####
export PATH=$PATHTOLARCH:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
$PATHTOLARCH/bin/python ppXAFS_auto_dev_pypt.py
