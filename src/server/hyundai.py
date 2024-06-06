# Client to query localhost:3000 for car state data
import datetime
import json

import requests

URL = "http://localhost:3000"
CACHE_TIMES = [6, 18]


class HyundaiClient:
    def __init__(self):
        pass

    def get_car_state(self):
        if self.cache_is_fresh():
            return self.cache
        else:
            response = requests.get(URL + "/car_state")
            if response.status_code == 200:
                response = response.json()
                cache = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": response,
                }
                self.save_cache(cache)
                return cache
            else:
                ValueError(f"Could not get car state: {response.status_code}")

    def get_battery_level(self):
        try:
            car_state = self.get_car_state()

            if car_state is None:
                raise ValueError("Could not get car state")

            return {
                "battery_level": car_state["data"]["evStatus"]["batteryStatus"],
                "timestamp": car_state["timestamp"],
            }
        except Exception as e:
            print(e)
            return {
                "battery_level": "??",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
    @property
    def cache(self):
        # Check if data/car_state.json exists
        try:
            with open("data/car_state.json", "r") as f:
                cache = json.load(f)
                return cache
        except FileNotFoundError:
            return None

    def cache_is_fresh(self):
        """
        Checks if the cache is fresh.
        The cache is fresh if the most recent cache time is reflected in the time stamp.
        The most recent cache time could be the most recent time in the same day or the last time in the previous day.
        :return:
        """
        now = datetime.datetime.now()
        past_cache_times = [x for x in CACHE_TIMES if x < now.hour]
        if self.cache is None:
            return False
        else:
            cache_time_string = self.cache["timestamp"]
            cache_time = datetime.datetime.strptime(
                cache_time_string, "%Y-%m-%d %H:%M:%S"
            )
            if now.day == cache_time.day:
                if past_cache_times[-1] <= cache_time.hour:
                    return True
            elif now.day == cache_time.day + 1:
                if CACHE_TIMES[-1] <= cache_time.hour and len(past_cache_times) == 0:
                    return True
        return False

    @staticmethod
    def save_cache(response):
        with open("data/car_state.json", "w") as f:
            json.dump(response, f)
