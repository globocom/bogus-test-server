import SimpleHTTPServer
import SocketServer
from threading import Thread


class BogusHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.request.sendall("HTTP/1.1 200")



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
