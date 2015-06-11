import druid

class Historical(druid.Druid):
    def classpath(self):
        import params
        return params.configs['druid']['hadoop.classpath']

    def name (self):
        return "historical"

if __name__ == "__main__":
    Historical().execute()
