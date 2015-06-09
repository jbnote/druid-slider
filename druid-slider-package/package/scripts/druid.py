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

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)

    # Dump the configuration dependent on the dictionary name
    node_type=name()
    PropertiesFile(format("{params.conf_dir}/{node_type}/runtime.properties"),
                   properties = params.configs[node_type],
                   owner=params.app_user)

    # Merge shared configuration with local one (or not ?)

    # XXX port is where ?
    process_cmd = format("{params.java64_home}/java -cp {params.config_dir}:{extra.classpath}:{params.app_root_dir}/current/lib/* -server {java.options} -Duser.timezone={user.timezone} -Dfile.encoding={file.encoding} io.druid.cli.Main server {name()} 2>{params.app_log_dir}/druid.err 1>{params.app_log_dir}/druid.out", **params.config['configurations']['druid'])

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
