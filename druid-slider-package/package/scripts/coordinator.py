import druid

class Coordinator(druid.Druid):
    def name (self):
        return "coordinator"

if __name__ == "__main__":
    Coordinator().execute()
