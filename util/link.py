from abc import ABCMeta, abstractmethod
from data_store import JSONDataStore
import os
import os.path
import json
from datetime import datetime

class Link:
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        self.settings = JSONDataStore(settings_file)
        self.settings.load()
        self.create_default_settings({"log_dir":"log/","received_log_file":"received.log","sent_log_file":"sent.log"})

    @abstractmethod
    def on_message_received(self, message):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    def get_settings(self):
        return self.settings

    def create_default_settings(self, default_settings):
        if self.get_settings().get_data() is None:
            self.get_settings().set_data({})
            
        for key in default_settings: 
            if key not in self.get_settings().get_data():
                update = {key:default_settings[key]}
                self.get_settings().get_data().update(update)

    def write_to_log(self, logfile, message):
        if os.path.isfile(logfile) == False:
            data = self.settings.get_data()
            logdir = data["log_dir"]
            os.system("mkdir -p " + logdir)
            os.system("touch " + logfile)            
        
        with open(logfile, "a") as f:
            log_dict = {}
            timestamp_dict = self.get_timestamp()
            log_dict.update(timestamp_dict)
            log_dict.update(message)
            f.write(json.dumps(log_dict) + "\r\n")

    def write_to_sent_log(self, message):
        data = self.settings.get_data()
        logfile = data["log_dir"] + "/" + data["sent_log_file"]
        self.write_to_log(logfile, message)

    def write_to_received_log(self, message):
        data = self.settings.get_data()
        logfile = data["log_dir"] + "/" + data["received_log_file"]
        self.write_to_log(logfile, message)

    def get_timestamp(self):
        time_dict = {"timestamp":{"utc":datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}}
        return time_dict
        
class URLLink(Link):
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        super(URLLink, self).__init__(settings_file)
        self.create_default_settings({"protocol":"http", "host":"localhost", "port":8000})

    def get_url(self):
        data = self.settings.get_data()
        url = data["protocol"] + "://" + data["host"] + ":" + str(data["port"])
        return url
    
class HTTPLink(URLLink):
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        super(HTTPLink, self).__init__(settings_file)
        self.create_default_settings({"page":"index.html"})
        

    def get_url(self):
        url = super(HTTPLink, self).get_url()
        data = self.settings.get_data()
        url = url + "/" + data["page"]
        return url
