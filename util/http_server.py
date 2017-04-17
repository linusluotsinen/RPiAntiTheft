from abc import ABCMeta, abstractmethod

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

from protocol import JSONQueryStringProtocol

import argparse
import urlparse

class GenericHttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = ""
        path = self.path
        if '?' in path:
            tmp_path, tmp = path.split('?', 1)            
            dictionary = urlparse.parse_qs(tmp)
            qs_str = ""
            for key in dictionary.keys():
                value = dictionary[key]
                qs_str = qs_str + key + "=" + value[0] + "&"
            qs = qs_str
        response = self.server.handler.process_qs(path, qs)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response)
     
class GenericHttpServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, handler):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.handler = handler
             
class HttpServerManager:
    def __init__(self, name, host, port, handler):
        self.name = name
        self.host = host
        self.port = port
        self.handler = handler
        self.server = None
         
    def start(self):
        self.server = GenericHttpServer((self.host, self.port), GenericHttpRequestHandler, self.handler)
        self.server.serve_forever()
    
    def stop(self):
        if self.server:
            self.server.shutdown()

class HttpServerHandler:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass
    
    @abstractmethod
    def get_protocol(self):
        pass
    
    @abstractmethod
    def process_qs(self, path, qs):
        pass

class EchoHttpServerHandler(HttpServerHandler):
    def __init__(self):
        super(EchoHttpServerHandler, self).__init__()
        self.protocol = JSONQueryStringProtocol()

    def get_protocol(self):
        return self.protocol
    
    def process_qs(self, path, qs):
        response = self.protocol.decode(qs)
        return response
    
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description="Run commands")
    parser.add_argument('-host', '--host', type=str, default="localhost",
                        help="Host")
    parser.add_argument('-p', '--port', default=8000, type=int,
                        help="Port")    
    args = parser.parse_args()
    
    print("Starting echo HTTP server...")
    server_handler = EchoHttpServerHandler()
    server = HttpServerManager("Echo HTTP Server", args.host, args.port, server_handler)
    server.start()
    
