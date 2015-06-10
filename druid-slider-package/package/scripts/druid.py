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

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)

    # Dump the configuration dependent on the dictionary name
    PropertiesFile(format("{params.config_dir}/_common/common.runtime.properties"),
                   properties = params.configs['_common'],
                   owner=params.app_user)

    node_type=self.name()
    node_config=params.configs[node_type]
    hostname=self.hostname()
    node_config.update({'druid.host':format("{hostname}:{node_config[druid.port]}")})
    PropertiesFile(format("{params.config_dir}/{node_type}/runtime.properties"),
                   properties = node_config,
                   owner=params.app_user)

    # Merge shared configuration with local one (or not ?)

    # XXX port is where ?
    conf = params.configs['druid']
    log_dir = params.app_log_dir
    process_cmd = format("{params.java64_home}/bin/java -cp {params.config_dir}/_common:{params.config_dir}/{node_type}:{conf[extra.classpath]} -server {conf[java.options]} -Duser.timezone={conf[user.timezone]} -Dfile.encoding={conf[file.encoding]} io.druid.cli.Main server {node_type} 2>{log_dir}/druid-{node_type}.err 1>{log_dir}/druid-{node_type}.out")

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
