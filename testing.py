import unittest

from server import app
from model import db, example_data, connect_to_db


class TrackerTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Mood and Activity Tracker", result.data)


if __name__ == "__main__":
    unittest.main()
