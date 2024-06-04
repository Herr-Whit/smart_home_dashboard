from unittest import TestCase

from src.server.tibber import TibberClient
from src.server.helpers import calculate_update_time


class TestTibberClient(TestCase):
    def test_get_price(self):
        client = TibberClient()
        response = client.get_price()
        self.assertIsNotNone(response)
        self.assertSetEqual({"current", "today", "tomorrow"}, set(response.keys()))
        self.assertEqual(24, len(response["today"]))
        self.assertEqual(24, len(response["tomorrow"]))
        print(response)


class Test(TestCase):
    def test_calculate_update_time(self):
        update_time = calculate_update_time(13, 15)
        self.assertIsNotNone(update_time)
        self.assertIsNotNone(update_time["target_time"])
        self.assertIsNotNone(update_time["time_to_sleep"])
        self.assertGreaterEqual(update_time["time_to_sleep"], 0)
