import argparse
import os
from util.reflection import Reflection
from util.data_store import JSONDataStore
from util.tmux import TmuxHandler
from util.gps_handler.gps_handler import GpsHandler
from util.gps_handler.gps_fence_handler import GpsFenceHandler
from sense_hat import SenseHat
import ast


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Run commands")   

    parser.add_argument('-name', '--name', default="Default", type=str,
                        help="Name of unit you are trying to protect")

    parser.add_argument('-link-module', '--link-module', default="qs_http_link", type=str,
                        help="Link module name")

    parser.add_argument('-client', '--client', default="QSHttpClient", type=str,
                        help="Client class name")

    parser.add_argument('-client-settings-file', '--client-settings-file', default="config/client.json", type=str,
                        help="Client settings file")

    parser.add_argument('-query', '--query', default=None, type=str,
                        help="Query server from client")

    parser.add_argument('-ping', '--ping', default=False, action="store_true",
                        help="Ping server.")

    parser.add_argument('-gps', '--gps', default=False, action="store_true",
                        help="Send GPS data to server.")

    parser.add_argument('-gps-fence-sync', '--gps-fence-sync', default=False, action="store_true",
                        help="This command will sync the gps fence data (retrieves the desired state from server).")

    parser.add_argument('-gps-fence-check', '--gps-fence-check', default=False, action="store_true",
                        help="This command will check fence status and fire events if needed.")
    
    parser.add_argument('-gps-fence-enable', '--gps-fence-enable', default=False, action="store_true",
                        help="This command will enable the gps fence.")

    parser.add_argument('-gps-fence-disable', '--gps-fence-disable', default=False, action="store_true",
                        help="This command will disable the gps fence.")

    parser.add_argument('-gps-fence-settings-file-client', '--gps-fence-settings-file-client', default="config/gps_fence_client.json", type=str,
                        help="GPS fence settings file for client")

    parser.add_argument('-gps-fence-settings-file-server', '--gps-fence-settings-file-server', default="config/gps_fence_server.json", type=str,
                        help="GPS fence settings file for server")

    parser.add_argument('-sensehat', '--sensehat', default=False, action="store_true",
                        help="Send sensehat data to server.")
    
    parser.add_argument('-server', '--server', default="QSHttpServer", type=str,
                        help="Server class name")
    
    parser.add_argument('-server-settings-file', '--server-settings-file', default="config/server.json", type=str,
                        help="Server settings file")
    
    parser.add_argument('-start-http-server', '--start-http-server', default=False, action="store_true",
                        help="Start server.")
    
    parser.add_argument('-kill-http-server', '--kill-http-server', default=False, action="store_true",
                        help="Start server.")
    
    args = parser.parse_args()

    reflection = Reflection()

    cls_client = reflection.get_class(args.link_module,args.client)
    client = cls_client(args.client_settings_file)
    
    #cls_server = reflection.get_class(args.link_module,args.server)
    #server = cls_server(args.server_settings_file)

    tmux = TmuxHandler()
    if args.start_http_server == True:
        print("Starting http server in tmux mode...")
        name = args.name + "_http"
        cmd = "python start_http_server.py -name " + name + " -server " + args.server + " -server-settings-file " + args.server_settings_file
        cmds = tmux.create_tmux_commands(name, cmd)
        os.system("\n".join(cmds))
        os.system("sleep 2")
    elif args.kill_http_server == True:
        name = args.name + "_http"
        print("Stopping http server running in tmux mode...")
        cmd = "tmux kill-session -t " + name
        os.system(cmd)

    if args.ping == True:
        cmd = {'command':'ping'}
        print client.send_message(cmd)

    sensor_data = {}
    if args.gps == True:
        gpsh = GpsHandler()
        gps_data = gpsh.get_gps_data()
        sensor_data.update({"gps": gps_data})
    
    if args.sensehat == True:
        sense = SenseHat()
        senshat_data = {}
        senshat_data.update(sense.get_orientation())
        weather = {'temperature':sense.get_temperature(), 'pressure':sense.get_pressure(), 'humidity':sense.get_humidity()}
        senshat_data.update(weather)
        sensor_data.update({"sensehat": senshat_data})
    
    if len(sensor_data) > 0:
        cmd = {'command':'log'}
        cmd.update(sensor_data)
        print client.send_message(cmd)

    if args.gps_fence_sync == True:
        cmd = {'command':'gps_fence_sync'}
        response, code = client.send_message(cmd)
        response = ast.literal_eval(response)
        if response['enabled'] == True:
            gpsh = GpsHandler()
            gps_data = gpsh.get_gps_data()
            response.update({"gps": gps_data})
        else:
            response.update({"gps": None})
        
        gpsfh_client = GpsFenceHandler(JSONDataStore(args.gps_fence_settings_file_client))
        gpsfh_client.get_settings().set_data(response);
        gpsfh_client.get_settings().save()

    if args.gps_fence_check == True:
        cmd = {'command':'gps_fence_check'}
        gpsfh_client = GpsFenceHandler(JSONDataStore(args.gps_fence_settings_file_client))
        gpsh = GpsHandler()
        gps_data = gpsh.get_gps_data()
        check = gpsfh_client.check_triggers(gps_data)
        cmd.update(check)
        response, code = client.send_message(cmd)
        
    if args.gps_fence_enable == True:
        gpsfh_server = GpsFenceHandler(JSONDataStore(args.gps_fence_settings_file_server))
        gpsfh_server.enable()

    if args.gps_fence_disable == True:
        gpsfh_server = GpsFenceHandler(JSONDataStore(args.gps_fence_settings_file_server))
        gpsfh_server.disable()
    
        
        
