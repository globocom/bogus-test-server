import unittest
import requests
from bogus.server import Bogus

class BogusTest(unittest.TestCase):

    def test_init_should_default_promiscuous_flag_to_True(self):
        b = Bogus()
        self.assertTrue(b.promiscuous)

    def test_init_with_promiscuous_false(self):
        b = Bogus(promiscuous=False)
        self.assertFalse(b.promiscuous)

    def test_serve_should_return_and_store_url(self):
        b = Bogus()
        url = b.serve()
        self.assertEqual(url, b.url)

    def test_serve_should_start_server_and_respond_to_any_request(self):
        b = Bogus()
        url = b.serve()
        response = requests.get("{}/something".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "")
        response = requests.get("{}/something-else".format(url))
        self.assertEqual(response.status_code, 200)
