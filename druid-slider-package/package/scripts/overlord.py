import druid

class Overlord(druid.Druid):
    def name (self):
        return "overlord"

if __name__ == "__main__":
    Overlord().execute()
