import unittest
from twitter_api import TwitterAPI

class TweeCase(unittest.TestCase):

    def setUp(self) -> None:
        self.api = TwitterAPI()
        return super().setUp()
    

    def test_isstring(self):
        self.assertIsInstance(self.api.consumer_key, str)
        self.assertIsInstance(self.api.consumer_secret, str)
        self.assertIsInstance(self.api.access_token, str)
        self.assertIsInstance(self.api.access_secret, str)

if __name__ == '__main__':
    unittest.main()