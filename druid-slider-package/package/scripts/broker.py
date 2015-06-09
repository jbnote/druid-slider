import druid

class Broker(druid.Druid):
    def name (self):
        return "broker"

if __name__ == "__main__":
    Broker().execute()
