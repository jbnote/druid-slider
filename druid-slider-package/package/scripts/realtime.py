import druid

class Realtime(druid.Druid):
    def name (self):
        return "realtime"

if __name__ == "__main__":
    Realtime().execute()
