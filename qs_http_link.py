from abc import ABCMeta, abstractmethod
from util.link import HTTPLink

class QSHttpClient(HTTPLink):
    def __init__(self, settings_file):
        super(QSHttpClient, self).__init__(settings_file)
          
    def on_message_received(self, message):
        pass

    
    def send_message(self, message):
        pass


class QSHttpServer(HTTPLink):
    def __init__(self, settings_file):
        super(QSHttpServer, self).__init__(settings_file)

    def on_message_received(self, message):
        pass

    def send_message(self, message):
        pass
