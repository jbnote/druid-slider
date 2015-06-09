#! /bin/bash

APPNAME=${1:-droya}
APPNUM=${2:-12}
slider flex $APPNAME --component DRUID_HISTORICAL $APPNUM --filesystem hdfs://root
