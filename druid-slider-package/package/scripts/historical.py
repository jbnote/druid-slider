import druid

class Historical(druid.Druid):
    def classpath(self):
        return self.hadoop_classpath()

    def name (self):
        return "historical"

if __name__ == "__main__":
    Historical().execute()
