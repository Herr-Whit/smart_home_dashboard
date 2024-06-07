from unittest import TestCase

from src.server.trash_collection import GoogleCalendarClient
client = GoogleCalendarClient()
items = client.get_next_trash_collection()

class TestGoogleCalendarClient(TestCase):
    def test_get_next_trash_collection(self):
        client = GoogleCalendarClient()
        items = client.get_next_trash_collection()
        print(items)

        self.assertIsNotNone(items)
