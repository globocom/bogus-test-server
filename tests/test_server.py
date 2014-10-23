import unittest
import requests
from bogus.server import Bogus, BogusHandler
from mock import Mock

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

    # intermitent?
    def test_serve_should_start_server_and_respond_to_any_request(self):
        b = Bogus()
        url = b.serve()
        response = requests.get("{}/something".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "")
        response = requests.get("{}/something-else".format(url))
        self.assertEqual(response.status_code, 200)


class BogusHandlerTest(unittest.TestCase):

    def setUp(self):
        self.request_mock = Mock()
        # mocks the request line, see http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5
        self.request_mock.makefile.return_value.readline.return_value = "GET /profile HTTP/1.1"

    def test_should_have_a_handle_method(self):
        bh = BogusHandler(self.request_mock, "client_address", "server")
        self.assertTrue(hasattr(bh, "handle"))

    def test_should_register_handlers(self):
        handler = ("/profile", lambda: ("Profile", 200))
        BogusHandler.register_handler(handler)
        self.assertIn(handler, BogusHandler.handlers["GET"])
        handler = ("/register", lambda: ("Register", 200))
        BogusHandler.register_handler(handler)
        self.assertIn(handler, BogusHandler.handlers["GET"])

        handler = ("/register", lambda: ("Register", 200))
        BogusHandler.register_handler(handler, method="POST")
        self.assertIn(handler, BogusHandler.handlers["POST"])

    def test_should_register_handler_and_respond_to_request_for_that_handler(self):
        BogusHandler.register_handler(("/profile", lambda: ("Profile", 200)))
        bh = BogusHandler(self.request_mock, "client_address", "server")
        bh.handle()
        expected_response = "HTTP/1.1 200 OK\r\nProfile"
        self.request_mock.sendall.assert_called_with(expected_response)
