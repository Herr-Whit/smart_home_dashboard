from unittest import TestCase

from src.server.hyundai import HyundaiClient


class TestHyundaiClient(TestCase):
    def test_get_car_state(self):
        client = HyundaiClient()
        state = client.get_car_state()
        print(state)

        self.assertIsNotNone(state)
