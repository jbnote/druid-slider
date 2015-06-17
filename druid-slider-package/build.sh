#! /bin/bash

DRUID_VERSION="0.7.3"
SOURCE=http://static.druid.io/artifacts/releases/druid-${DRUID_VERSION}-bin.tar.gz
TARGET=$HOME/$(basename $SOURCE)

CONFIGS="appConfig.json resources.json"

wget $SOURCE -O $TARGET

# XXX rebuild the tarball by adding the dependencies
tar zxf $TARGET
DRUID_DIR=druid-${DRUID_VERSION}
pushd druid-${DRUID_VERSION}
java -cp config/_common:lib/* -Ddruid.extensions.localRepository=m2 -Ddruid.extensions.coordinates='["io.druid.extensions:druid-kafka-eight","io.druid.extensions:druid-hdfs-storage","io.druid.extensions:mysql-metadata-storage"]' -Ddruid.extensions.remoteRepositories="[ \"file://$HOME/.m2/repository\", \"https://repo1.maven.org/maven2\", \"https://metamx.artifactoryonline.com/metamx/pub-libs-releases-local\", \"https://repository.cloudera.com/artifactory/cloudera-repos\" ]" io.druid.cli.Main tools pull-deps
popd
NEWTAR=../$(basename $SOURCE)
tar zcf $NEWTAR $DRUID_DIR
rm -Rf $DRUID_DIR

mvn clean install -DskipTests -Ddruid.src=$NEWTAR -Ddruid.version=$DRUID_VERSION
unzip -o target/druid-slider-package-0.1.zip appConfig.json resources.json
