DRUID On YARN
=============

### Goals

  * Use capabilities of YARN for Druid management

DRUID as YARN application using Slider
--------------------------------------

### Build

Checkout Slider code (https://github.com/apache/incubator-slider)
```sh
git clone git@github.com:apache/incubator-slider.git
git checkout -b slider-0.80.0-incubating remotes/origin/releases/slider-0.80.0-incubating
```
The Slider version you checked out needs to match ${slider.version} in pom.xml

Artifacts:
 - Slider application package: __`target/koya-slider-package-0.1.zip`__

####Install Slider

### Configure KOYA application package

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