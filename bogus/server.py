import SimpleHTTPServer
import SocketServer
from threading import Thread


class BogusHandler(SocketServer.StreamRequestHandler):
    """
    Custom handler to use in TCPServer.
    This handler has hability to map requests to registered handler callers.
    It doesn't check anything about the request, unless you don't send a method or a
    status code, which we need to map the handler to the request being made.
    """

    def handle(self):
        """
        Handles requests by parsing them and finding if there's any handlers registered to
        handle them, if it doesn't find any handlers and promiscuous is set to True, it
        responds with an empty body and a 200 status code, if promiscuous is set to False
        it returns an empty body and a 404 status code.
        """
        self.raw_requestline = self.rfile.readline(65537)
        self.parse_request()

        handler = self.find_handler()
        if handler:
            # TODO: validate handler output
            body, status = self._call_handler(handler)
            response = "HTTP/1.1 {0} OK\r\n{1}".format(status, body)
            self.response = response
            self.request.sendall(response)
            return

        self.response = "HTTP/1.1 200 OK"
        self.request.sendall(self.response)

    def _call_handler(self, handler, *args):
        response = handler()
        if type(response) is not tuple:
            raise ValueError("handler function should return 2 arguments.")
        if len(response) != 2:
            raise ValueError("handler function should return 2 arguments.")
        if type(response[1]) is not int:
            raise ValueError("handler function second return type must be an integer indicating the status code.")

        return response


    def find_handler(self):
        if not hasattr(self, "handlers"):
            return False

        if not self.method in self.handlers.keys():
            return False
        else:
            for path, handler in self.handlers[self.method]:
                if path == self.path:
                    return handler

    def parse_request(self):
        """
        Parses the request first line to get the status and method.
        Saves it on instances variables.
        """
        reqline = self.raw_requestline.rstrip('\r\n')
        self.requestline = reqline

        words = reqline.split()
        if len(words) == 3:
            method, path, _ = words
        elif len(words) == 2:
            method, path = words
        else:
            self.send_error(400, "Bad request syntax (%r)" % requestline)
            return

        self.method = method
        self.path = path


    @classmethod
    def register_handler(cls, handler, method="GET"):
        """
        Register a handler within a given method, the default method is get.
        The data structure used to store the handler is a dictionary of arrays, each array
        entry contains the handler tuple (path, callable). It looks like this:
            {"GET": ("/profile", profileHandler), ("/settings", settingsHandler)}
        The registered handler should return 2 values, the response body and status code.
        """
        if not hasattr(cls, "handlers"):
            cls.handlers = {method: [handler]}
        elif method in cls.handlers.keys():
            cls.handlers[method].append(handler)
        else:
            cls.handlers[method] = [handler]


class Bogus(object):

    def __init__(self, promiscuous=True):
        self.promiscuous = promiscuous

    """
    Starts up the HTTP server.
    """
    def serve(self):
        httpd = SocketServer.TCPServer(("127.0.0.1", 0), BogusHandler)
        thread = Thread(target=httpd.serve_forever)
        thread.setDaemon(True)
        thread.start()
        while not thread.is_alive():
            continue
        self.url = "http://{0}:{1}".format(httpd.server_address[0], httpd.server_address[1])
        return self.url

    def register(self, handler, method="GET"):
        BogusHandler.register_handler(handler, method)
