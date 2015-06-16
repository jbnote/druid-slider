#! /bin/bash

APPNAME=${1:-droya}
APPNUM=${2:-3}
APPTYPE=${3:-"REALTIME"}
slider flex $APPNAME --component DRUID_${APPTYPE} $APPNUM --filesystem hdfs://root
