DRUID On YARN
=============

### Goals

  * Use capabilities of YARN for Druid management

DRUID as YARN application using Slider
--------------------------------------

### Prerequisites

## READ THIS

You can't run druid by itself and will need to do minimal setup in
order to get druid to run.

## Metadata store

Druid on slider running on a real cluster cannot use the integrated
derby DB by default and is therefore configured to use a mysql store
by default. You should need:

* a mysql host accessible (property site.druid.mysql.host, default mysql);
* a database within this mysql (property site.druid.mysql.database, default druid);
* table creation rights within this database for the connecting user (property site.druid.metadata.storage.connector.user, default druid with password site.druid.metadata.storage.connector.password)

Work is underway to allow Phoenix to act as a metadata store, which would allow all of Druid's state to be stored on HDFS.

## GUICE plugins

Druid extensions (at least druid-hdfs-storage, mysql-metadata-storage
are needed) use guice to download dependencies from maven. The default
configuration needs internet access and takes a long time to run, see:
http://druid.io/docs/latest/Including-Extensions.html

The build.sh script packages some dependencies in the druid tarball so
you don't have to download them. Startup time is considerably improved
and you don't need internet access.

You can also setup site._common.druid.extensions.remoteRepositories to
point to a local nexus mirror.

## Realtime nodes

You cannot run realtime nodes without configuring their specFile,
therefore, they are not enabled by default.


### Build

Edit ${slider.version} in pom.xml to match the slider version you installed

Build slider with:
mvn clean install -DskipTests -Ddruid.src=$NEWTAR -Ddruid.version=$DRUID_VERSION

Artifacts:
 - Slider application package: __`target/druid-slider-package-0.1.zip`__

####Install Slider

### Configure druid-slider application package

If you use the full archive, the configuration file templates are already in your working directory. Otherwise extract them from the Slider package.

####appConfig.json

Extract the packaged configuration files you are going to customize:
```
unzip druid-slider-package-0.1.zip appConfig.json resources.json
```
Adjust following properties in the global section:
```
    "application.def": "druid-slider-package-0.1.zip",
    "site.druid.zookeeper.connect": "${ZK_HOST}"
```
Above will be used to configure server.properties and launch the Druid servers. All properties prefixed with `site.druid-broker.` will be set in the server.properties file supplied with the archive. Only non-default settings need to be defined here.

####resources.json

Configure the number of servers and other resource requirements:
```
  "components" : {
    "DRUID_BROKER" : {
      "yarn.component.instances" : "5",
    },
    "DRUID_HISTORICAL" : {
      "yarn.component.instances" : "2",
    },
    "DRUID_REALTIME" : {
      "yarn.component.instances" : "3",
    }
```
More information about the application configuration can be found [here](http://slider.incubator.apache.org/docs/configuration/core.html).

### Deploy DRUID Cluster

See example deploy.sh script
