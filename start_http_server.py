import argparse
import os
from util.reflection import Reflection
from util.http_server import HttpServerManager

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description="Run commands")
    
    parser.add_argument('-server', '--server', default="QSHttpServer", type=str,
                        help="Server class name")
    parser.add_argument('-server-settings-file', '--server-settings-file', default="config/server.json", type=str,
                        help="Server settings file")
    parser.add_argument('-name', '--name', default="Default", type=str,
                        help="Name of unit you are trying to protect")
    parser.add_argument('-link-module', '--link-module', default="qs_http_link", type=str,
                        help="Link module name")
    args = parser.parse_args()
    
    
    reflection = Reflection()
    cls_server = reflection.get_class(args.link_module,args.server)
    server = cls_server(args.server_settings_file)

    host = server.get_settings().get_data()["host"]
    port = server.get_settings().get_data()["port"]
    
    handler = server.get_handler()
    server = HttpServerManager(args.name, host, port, handler)
    server.start()
