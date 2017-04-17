import argparse
from util.reflection import Reflection
from util.data_store import JSONDataStore


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Run commands")   


    parser.add_argument('-link-module', '--link-module', default="qs_http_link", type=str,
                        help="Link module name")

    parser.add_argument('-client', '--client', default="QSHttpClient", type=str,
                        help="Client class name")

    parser.add_argument('-client-settings-file', '--client-settings-file', default="config/client.json", type=str,
                        help="Client settings file")

    parser.add_argument('-server', '--server', default="QSHttpServer", type=str,
                        help="Server class name")

    parser.add_argument('-server-settings-file', '--server-settings-file', default="config/server.json", type=str,
                        help="Server settings file")
    
    #parser.add_argument('-build-config', '--build-config', default=False, action="store_true",
    #                    help="Build configuration files for the application.")
    
    args = parser.parse_args()

    reflection = Reflection()

    cls_client = reflection.get_class(args.link_module,args.client)
    client = cls_client(args.client_settings_file)
    
    cls_server = reflection.get_class(args.link_module,args.server)
    server = cls_server(args.server_settings_file)
    
    #if args.build_config == True:
    #    pass
