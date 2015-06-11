import druid

class Realtime(druid.Druid):
    def classpath(self):
        import params
        return params.configs['druid']['hadoop.classpath']

    def name (self):
        return "realtime"

if __name__ == "__main__":
    Realtime().execute()
