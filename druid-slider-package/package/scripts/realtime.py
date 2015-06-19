from resource_management import *
import druid

class Realtime(druid.Druid):
    def classpath(self):
        return self.hadoop_classpath()

    def name(self):
        return "realtime"

    def specfile(self):
        import params
        return format("{params.config_dir}/realtime/realtime.spec")

    def gettypeconf(self):
        baseconfig=super(Realtime, self).gettypeconf()
        baseconfig.update({'druid.realtime.specFile':self.specfile()})
        return baseconfig

    def getspec(self):
        import params
        # Download this file and use it as a spec file
        source_file=params.configs['realtime']['druid.realtime.specFile']
        File(self.specfile(),
             owner=params.app_user,
             mode=0644,
             content=InlineTemplate(DownloadSource(source_file).get_content()))

    def writeconf(self, env):
        self.getspec()
        super(Realtime, self).writeconf(env)

if __name__ == "__main__":
    Realtime().execute()
