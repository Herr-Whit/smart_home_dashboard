from unittest import TestCase

from src.tibber_client import TibberClient


class TestTibberClient(TestCase):
    def test_get_price(self):
        client = TibberClient()
        response = client.get_price()
        self.assertIsNotNone(response)
        self.assertSetEqual({'current', 'today', 'tomorrow'}, set(response.keys()))
        self.assertEqual(24, len(response['today']))
        self.assertEqual(24, len(response['tomorrow']))
        print(response)