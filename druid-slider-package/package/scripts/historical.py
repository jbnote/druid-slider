import druid

class Historical(druid.Druid):
    def name (self):
        return "historical"

if __name__ == "__main__":
    Historical().execute()
