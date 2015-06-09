#! /bin/bash

APPNAME=${1:-droya}
slider package --install --replacepkg --name DRUID --package target/druid-slider-package-0.1.zip
for action in stop destroy; do
    slider $action $APPNAME
done
# Will mirror with source defined in appConfig-mirror.json -- may need customization
unzip -o target/druid-slider-package-0.1.zip appConfig.json resources.json metainfo.xml
slider create ${APPNAME} --debug --filesystem hdfs://root --queue dev --template appConfig.json --resources resources.json
