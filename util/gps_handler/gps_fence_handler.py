#from gps_handler import GpsHandler
import math

class GpsFenceHandler:
    def __init__(self, settings):
        self.settings = settings
        self.settings.load()
        if self.settings.get_data() is None:
            #gpsh = GpsHandler()
            #gps_data = gpsh.get_gps_data()
            default_settings = {"enabled": False, "thresholds":{"dist":100,"speed":10}, "gps":None }
            self.settings.set_data(default_settings)
            self.settings.save()

    def enable(self):
        data = self.settings.get_data()
        data["enabled"] = True
        self.settings.save()

    def disable(self):
        data = self.settings.get_data()
        data["enabled"] = False
        data["gps"] = None
        self.settings.save()

    #def refresh(self, client):
    #    data = self.settings.get_data()
    #    gpsh = GpsHandler()
    #    gps_data = gpsh.get_gps_data()
    #    data["gps"] = gps_data
    #    self.settings.save()

    def get_settings(self):
        return self.settings    

    def distance(self,lat1, lon1, lat2, lon2):
       radius = 6371*1000 # m

       dlat = math.radians(lat2-lat1)
       dlon = math.radians(lon2-lon1)
       a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
           * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
       c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
       d = radius * c
       return d
    
    def check_triggers(self, gps_data):
        ret = {"dist": False, "speed": False }
        thresholds = self.settings.get_data()["thresholds"]
        state = self.settings.get_data()["gps"]
        
        if state is not None:
            dist = self.distance(state['latitude'],state['longitude'],gps_data['latitude'],gps_data['longitude'])
            if dist > thresholds['dist']:
                ret["dist"] = True

            if state["speed"] > thresholds["speed"]:
                ret["speed"] = True
        return ret
        
   
   
