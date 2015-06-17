DRUID as YARN application using Slider
======================================

## Prerequisites

You can't run druid by itself and will need to do minimal setup in
order to get druid to run.

### Metadata store

Druid on slider running on a real cluster cannot use the integrated
derby DB by default and is therefore configured to use a mysql store
by default. You should need:

* a mysql host accessible (`site.druid.mysql.host`, default mysql);
* a database within this mysql (`site.druid.mysql.database`, default druid);
* table creation rights within this database for the connecting user (`site._common.druid.metadata.storage.connector.user`, default druid with password `site._common.druid.metadata.storage.connector.password`, default none)

Work is underway to allow Phoenix to act as a metadata store, which would allow all of Druid's state to be stored on HDFS.

### GUICE plugins
Druid extensions (at least druid-hdfs-storage, mysql-metadata-storage
are needed) use guice to download dependencies from maven. The default
configuration needs internet access and takes a long time to run. This is a [known issue].
[known issue]::http://druid.io/docs/latest/Including-Extensions.html

The `build.sh` script packages some dependencies in the druid tarball so
you don't have to download them. Startup time is considerably improved
and you don't need internet access.

You can also setup `site._common.druid.extensions.remoteRepositories` to
point to a local nexus mirror.

## Realtime nodes

You cannot run realtime nodes without configuring their specFile,
therefore, they are not enabled by default.

### Build

Edit `slider.version` in pom.xml to match the slider version you installed

Build slider with:
```sh
$ mvn clean install -DskipTests -Ddruid.src=$DRUID_TARBALL_PATH -Ddruid.version=$DRUID_VERSION
```
The resulting slider application package lives in __`target/druid-slider-package-0.1.zip`__

### Configure druid-slider application package

If you use the `build.sh` script, the configuration file templates are
already in your working directory. Otherwise extract them from the
slider package zipfile:
```sh
unzip druid-slider-package-0.1.zip appConfig.json resources.json
```

####appConfig.json

Adjust following properties in the global section:
```json
        "site.druid.mysql.host": "mysql",
        "site.druid.mysql.database": "druid",
        "site._common.druid.metadata.storage.connector.user": "druid",
        "site._common.druid.metadata.storage.connector.password": "",
        "site.druid.zookeeper.connect": "${ZK_HOST}",
```

Above will be used to configure specific `runtime.properties` files
and launch the Druid servers. For instance all properties prefixed
with `site.realtime.` will be set in the
`config/realtime/runtime.properties` file.

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

### Deploy

The `deploy.sh` script provides an example of how to deploy.

