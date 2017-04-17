from gps_controller import GpsController
import time

class GpsHandler:
   def get_gps_data(self):
      gpsc = GpsController()
      gpsc.start()
      time.sleep(2)
      
      googlemaps = 'http://maps.google.com/maps?q=loc:' + str(gpsc.fix.latitude) +',' + str(gpsc.fix.longitude) + '&z=17'
      data = {'utc': gpsc.utc, 'latitude': gpsc.fix.latitude, 'longitude': gpsc.fix.longitude, 'altitude': gpsc.fix.altitude, 'speed': gpsc.fix.speed, 'google_maps_link': googlemaps}

      gpsc.stopController()
      gpsc.join()
      
      return data

if __name__ == '__main__':
   gpsh = GpsHandler()
   print gpsh.get_gps_data()
