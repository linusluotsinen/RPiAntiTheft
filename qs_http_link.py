from abc import ABCMeta, abstractmethod
from util.link import HTTPLink
from util.http_server import HttpServerHandler
from util.http_query import HTTPQuery
from util.protocol import JSONQueryStringProtocol

class QSHttpClient(HTTPLink):
    def __init__(self, settings_file):
        super(QSHttpClient, self).__init__(settings_file)
        self.query = HTTPQuery()
        self.protocol = JSONQueryStringProtocol()
    
    def send_message(self, message):
        qs = protocol.encode(message)
        url = self.get_url()
        url = url + "?" + qs
        response, response_code = self.query.query(url)
        if response_code == 200:
            pass

    def on_message_received(self, message):
        pass
    
class QSHttpServerHandler(HttpServerHandler):
    def __init__(self, link):
        super(QSHttpServerHandler, self).__init__()
        self.protocol = JSONQueryStringProtocol()
        self.link = link

    def get_protocol(self):
        return self.protocol
    
    def process_qs(self, path, qs):
        message = self.protocol.decode(qs)
        response = self.link.on_message_received(message)
        return response

class QSHttpServer(HTTPLink):
    def __init__(self, settings_file):
        super(QSHttpServer, self).__init__(settings_file)
        self.handler = QSHttpServerHandler(self)

    def get_handler(self):
        return self.handler

    def send_message(self, message):
        pass

    def on_message_received(self, message):
        if 'command' in message:
            cmd = message['command']
            if cmd == 'log':
                pass
            elif cmd == 'gps_fence':
                pass
            
