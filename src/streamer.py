from lightstreamer.client import LightstreamerClient, Subscription
import time
from datetime import datetime, timedelta


class ISSListener:
    def __init__(self):
        # Initialize quantities and their previous values
        self.quantities = {
            "NODE3000005": None,  # Urine quantity
            "NODE3000009": None,  # Clean quantity
            "NODE3000008": None,  # Waste quantity
        }

        # Track previous values and timestamps of increases
        self.previous_values = {key: None for key in self.quantities.keys()}
        self.last_increase_times = {key: None for key in self.quantities.keys()}

        # Initialize Lightstreamer client and subscription
        self.client = LightstreamerClient("https://push.lightstreamer.com", "ISSLIVE")
        self.subscription = Subscription(
            mode="MERGE",
            items=list(self.quantities.keys()),
            fields=["Value"],
        )
        self.subscription.addListener(self)
        self.client.subscribe(self.subscription)
        self.client.connect()

    def onItemUpdate(self, update):
        item_name = update.getItemName()
        if item_name in self.quantities:
            new_value = float(update.getValue("Value"))
            previous_value = self.previous_values[item_name]

            # Check if the value has increased
            if previous_value is not None and new_value > previous_value:
                self.last_increase_times[item_name] = datetime.now()

            # Update the previous value
            self.previous_values[item_name] = new_value
            self.quantities[item_name] = new_value

    def get_latest_value(self):
        return tuple(self.quantities.values())

    def get_recent_increases(self):
        # Define what "recent" means (e.g., within the last minute)
        recent_threshold = datetime.now() - timedelta(minutes=1)

        # Check for recent increases
        recent_increases = {
            "NODE3000005": False,  # Urine
            "NODE3000009": False,  # Clean
            "NODE3000008": False,  # Waste
        }

        for item_name, last_increase_time in self.last_increase_times.items():
            if last_increase_time and last_increase_time >= recent_threshold:
                recent_increases[item_name] = True

        return tuple(recent_increases.values())


if __name__ == "__main__":
    listener = ISSListener()

    while True:
        print("Latest values:", listener.get_latest_value())
        print("Recent increases:", listener.get_recent_increases())
        time.sleep(1)