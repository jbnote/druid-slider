import logging
import sys
import os
import inspect
import pprint
from resource_management import *

logger = logging.getLogger()

class Druid(Script):

  def name(self):
    return "unknown"

  def install(self, env):
    self.install_packages(env)

  def configure(self, env):
    import params
    env.set_params(params)

  def hostname(self):
    import socket
    return socket.getfqdn()

  def gettypeconf(self):
    import params
    node_config=params.configs[self.name()]
    hostname=self.hostname()
    node_config.update({'druid.host':format("{hostname}:{node_config[druid.port]}")})
    return node_config

  def writeconf(self, env):
    import params
    # Dump the configuration dependent on the dictionary name
    PropertiesFile(format("{params.config_dir}/_common/common.runtime.properties"),
                   properties = params.configs['_common'],
                   owner=params.app_user)

    node_type=self.name()
    PropertiesFile(format("{params.config_dir}/{node_type}/runtime.properties"),
                   properties = self.gettypeconf(),
                   owner=params.app_user)

    for log in ['log4j', 'log4j2']:
      File(format("{params.config_dir}/_common/{log}.xml"),
           mode=0644,
           owner=params.app_user,
           content=Template(format("{log}.xml.j2"),
                            loglevel=params.configs['log4j']['loglevel'],
                            filename=format("{params.app_log_dir}/druid-{node_type}.log")))


  def hadoop_classpath(self):
    import subprocess
    return subprocess.Popen(["hadoop", "classpath"], stdout=subprocess.PIPE).communicate()[0].rstrip()

  def classpath(self):
    return ""

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    self.writeconf(env)

    node_type=self.name()
    conf = params.configs['druid']
    log_dir = params.app_log_dir
    classpath = self.classpath()
    process_cmd = format("{params.java64_home}/bin/java -Djava.io.tmpdir={conf[java.io.tmpdir]} -cp {params.config_dir}/_common:{params.config_dir}/{node_type}:{params.app_root}/lib/*:{classpath} -server {conf[java.options]} -Duser.timezone={conf[user.timezone]} -Dfile.encoding={conf[file.encoding]} io.druid.cli.Main server {node_type} 2>{log_dir}/druid-{node_type}.err 1>{log_dir}/druid-{node_type}.out")

#    if params.configs['global']['http_proxy'] != None:
#      for var in ['http_proxy', 'HTTP_PROXY']:
#        os.environ[var] = params.configs['global']['http_proxy']

    Execute(process_cmd,
            user=params.app_user,
            logoutput=True,
            wait_for_finish=False,
            pid_file=params.pid_file)

  def stop(self, env):
    import params
    env.set_params(params)
    pid = format("`cat {pid_file}` >/dev/null 2>&1")
    Execute(format("kill {pid}"),
            user=params.app_user
    )
    Execute(format("kill -9 {pid}"),
            ignore_failures=True,
            user=params.app_user
    )
    Execute(format("rm -f {pid_file}"),
            user=params.app_user)

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.pid_file)

if __name__ == "__main__":
  Druid().execute()
