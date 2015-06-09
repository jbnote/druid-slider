from resource_management import *
import os

config = Script.get_config()
configs = config['configurations']

app_root = config['configurations']['global']['app_root']
java64_home = config['hostLevelParams']['java_home']
app_user = config['configurations']['global']['app_user']
pid_file = config['configurations']['global']['pid_file']
app_log_dir = config['configurations']['global']['app_log_dir']
druid_version = config['configurations']['global']['druid_version']

config_dir = format("{app_root}/config")
