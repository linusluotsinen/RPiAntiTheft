from abc import ABCMeta, abstractmethod
from data_store import JSONDataStore

class Link:
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        self.settings = JSONDataStore(settings_file)
        self.settings.load()

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

class URLLink(Link):
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        super(URLLink, self).__init__(settings_file)
        self.create_default_settings({"protocol":"http", "host":"localhost", "port":"80"})

    def get_url(self):
        data = self.settings.get_data()
        url = data["protocol"] + "://" + data["host"] + ":" + data["port"]
        return url
    
class HTTPLink(URLLink):
    __metaclass__ = ABCMeta

    def __init__(self, settings_file):
        super(HTTPLink, self).__init__(settings_file)
        self.create_default_settings({"page":"index.html"})
        if self.settings.is_file() == False:
            self.settings.save()

    def get_url(self):
        url = super(HTTPLink, self).get_url()
        data = self.settings.get_data()
        url = url + "/" + data["page"]
