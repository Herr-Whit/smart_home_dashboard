from unittest import TestCase

from src.tibber_client import TibberClient


class TestTibberClient(TestCase):
    def test_get_price(self):
        client = TibberClient()
        response = client.get_price()
        print(response)
