#! /bin/bash

SOURCE=http://static.druid.io/artifacts/releases/druid-0.7.3-bin.tar.gz
TARGET=$HOME/$(basename $SOURCE)
VERSION=$(echo $TARGET | cut -d'-' -f2)

CONFIGS="appConfig.json resources.json"

wget $SOURCE -O $TARGET
mvn clean install -DskipTests -Ddruid.src=$TARGET -Ddruid.version=$VERSION
unzip -o target/druid-slider-package-0.1.zip appConfig.json resources.json
