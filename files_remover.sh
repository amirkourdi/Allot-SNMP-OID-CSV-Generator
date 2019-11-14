#!/bin/bash

find /opt/sybase/data/KPIs/tools/output -iname "*.csv" -atime 7 | xargs rm -rf
