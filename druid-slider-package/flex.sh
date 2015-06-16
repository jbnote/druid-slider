#! /bin/bash

APPNAME=${1:-droya}
APPNUM=${2:-3}
slider flex $APPNAME --component DRUID_REALTIME $APPNUM --filesystem hdfs://root
slider flex $APPNAME --component DRUID_HISTORICAL $APPNUM --filesystem hdfs://root
